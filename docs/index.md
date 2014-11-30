The VNC roll documentation
==============================

Description
------------------------------

The VNC roll provides a remote desktop service on the Rocks cluster within a
browser.  This web interface is based on HTML5 and JavaScript and works on all major browsers.
Native clients is also supported.

Usage
-----------------------------
Open the url http://frontend.name/vnc.html and follow the link.
A native client can connect to fronted.name:5901.

Installation
--------------------
Download the precompiled roll from [https://github.com/dragz/vnc-roll/releases](https://github.com/dragz/vnc-roll/releases)

and run the following sequence of commands

```
# cd /export/rocks/install
# rocks add roll /tmp/vnc-1.0.0.x86_64.iso
# rocks enable roll vnc
# rocks create distro
# rocks run roll vnc | sh
# reboot
```

Links
----------

Documentation: [http://vnc-roll.readthedocs.org/](http://vnc-roll.readthedocs.org/)

Source:  [http://github.com/dragz/vnc-roll](http://github.com/dragz/vnc-roll)

