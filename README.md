# Facebook backported RPMs for CentOS

This repo contains a number of RPM packages that we backported to CentOS 7 and 
run in our infrastructure. Most of these packages have dependencies from EPEL 
and from the last released CentOS 7 point release. Some packages also have 
extra dependencies from Fedora Rawhide that we list below. Because we pull from
Rawhide, some of these versions may no longer be available; in that case it's 
usually safe to use the latest release, but feel free to file an issue as well.
In our environment we import the `src.rpm` for these dependencies and rebuild
them in [mock](https://github.com/rpm-software-management/mock).

## Dependencies

`systemd` depends on the `dbus`, `python34-csselect`, `python34-lxml`, and
`util-linux` packages from this repo. It also requires the following packages
from Rawhide:
* curl-7.49.0-1.fc25
* dracut-044-75.fc25
* kmod-22-4.fc25
* libgudev-230-2.fc23

`mkosi` requires the following packages from Rawhide:
* arch-install-scripts-15-3.fc24
* archlinux-keyring-20160215-1.fc25
* debootstrap-1.0.81-1.fc24
* keyrings-filesystem-1-5.fc24
* python35-3.5.2-3.fc23

## Contribute

See the CONTRIBUTING file for how to help out.

## License

The RPM specfiles in this repository are released under the MIT license. See
LICENSE for more details.
