==================================
The VNC Roll
==================================

Remote desktop service for Rocks Clusters.


Description
===========
The VNC roll installs and configure a remote desktop service based on TigerVNC and
NoVNC that will enable users to run graphical user interfaces on the cluster
without any local software on the client machine than a modern browser that
JavaScript and HTML5.  Google Chrome, Firefox, Safari and Internet Explorer are
supported by this setup.  It is even possible to use the service on devices
without physical keyboard and mouse like tablets and mobile phones, but the 
X desktops are kind of clunky and not very usable on such devices.

Technical details
=================

The setup consists of several services chained together to make the service both
easy to use for non Linux clients and at the same time have sufficient security.
Remark, this service bypasses the ssh-login security by opening up a new graphical login
service on the cluster.  The security is maintained by encrypting the external connection
with stunnel and access to the service is done through tcp-wrapper.  The service is
restricted to the public ip-range set by the rocks installation. The contrib/whitelisting dir
has a description on how to automatically open up the service to IPs that make successful logins
to the cluster.

Chain of services
------------------

Web client:

```
Client web browser -> frontend port 6080 -> stunnel to port localhost:6081 -> novnc to localhost:5902 -> xinetd start Xvnc.
```

Native vnc client:

```
Native client -> frontend port 5901 -> xinetd start Xvnc with native encryption VENcrypt.
```

Both stunnel and xinetd checks /etc/hosts.allow if the client is whitelisted.  Native vnc clients can be found on the TigerVNC
homepage.

Installation
============

Add the roll at frontend installation or afterwards using the standard method described in the Rocks docs.

Usage
======

Point your browser to http://frontend.name/vnc/ and you will be set to go.

All login nodes will also get the vnc setup upon reinstall after roll installation.



Links
=======

Rocks:    http://www.rocksclusters.org/

NoVNC:    https://github.com/kanaka/novnc

TigerVNC: http://www.tigervnc.org/

Authors
========

Roy Dragseth, roy.dragseth@uit.no

Jonas Juselius, jonas.juselius@uit.no

