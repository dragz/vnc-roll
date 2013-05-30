#!/usr/bin/python
# this program is called by rsyslogd whenever the /etc/rsyslog.d/sshlog.conf
# detects a successful login on stallo-gui.

import os, sys, time, shelve, re, signal

# time window for allowed vnc connection after successful login
ALLOWED_TIMEOUT=5*60
#
#  Default allowed domains, eg. norwegian academic networks and partners
#
allowed_domains = ["129.242.0.0/255.255.0.0","10.1.0.0/255.255.0.0"]

# tmp file that will be copied to the vnc servers.
hostsallow="/tmp/hosts.allow"

# allowstate contains the state between runs.
# it is a dict with { ip : timestamp} entries. If timestamp is too old
# the entry will be deleted from allowstate and hosts.allow.
allowstate=shelve.open("/var/spool/hosts.allow.shelve")

header="""#
# hosts.allow   This file contains access rules which are used to
#               allow or deny connections to network services that
#               either use the tcp_wrappers library or that have been
#               started through a tcp_wrappers-enabled xinetd.
#
#               See 'man 5 hosts_options' and 'man 5 hosts_access'
#               for information on rule syntax.
#               See 'man tcpd' for information on tcp_wrappers
#
# Do not edit manually, this file is overwritten automatically
# when new ssh logins is coming into stallo-gui.
"""


allowtemplate = "Xvnc : %s : ALLOW\n"
denyall = "Xvnc : ALL : DENY\n"

#
#  debug stuff, stdout/stderr goes into /dev/null under rsyslog.
#
sys.stderr = open("/tmp/foo","w")
file("/tmp/hostallowdebug.txt","w").write("")
debug = lambda s : file("/tmp/hostallowdebug.txt","a").write(s+"\n")


def copyfiles(fn):
    copy="seq 1 16 | xargs -i -P 16 scp %s stallo-vnc-{}:/etc/"%fn
#    copy="scp %s stallo-gui:/etc/" % fn
    os.system(copy)

#
# For some reason the signal stuff doesn't work when run under rsyslog
# just comment out and see if we can make it work later.  The intention was
# to have a read timeout so one could clear old entries automatically, as it is now
# old entries are only cleared when new logins appear.  Not a big problem, fix later.
#
#def handler(signum, frame):
    #debug("Signal handler called")
    #raise IOError("Read timeout")

#signal.signal(signal.SIGALRM, handler)

state_changed = None
text = header
for domain in allowed_domains:
    text +=  allowtemplate % domain

try:
    ip = None
    #alarm = signal.alarm(ALLOWED_TIMEOUT)
    debug("waiting for input")
    logline = sys.stdin.readline()
    debug("got input")
    #signal.alarm(0)
    ip = re.match(".* (\d+\.\d+\.\d+\.\d+) .*", logline).groups()[0]
    debug(ip)
except EOFError:
    pass
except AttributeError:
    debug("cannot find ip "+logline)
except IOError:
    # We got a read timeout
    debug("read timeout")

now = time.time()
if ip:
    allowstate[ip] = now
    state_changed = 1
    
for i, ts in allowstate.items():
    debug(str([i, now, ts]))
    if now - ts < ALLOWED_TIMEOUT:
        text += allowtemplate % i
    else:
        del allowstate[i]
        state_changed = 1
        
text += denyall
    
if state_changed:
    file(hostsallow, "w").write(text)
    allowstate.sync()
    copyfiles(hostsallow)

