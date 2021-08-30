# Where did the packages go?

This repository is no longer being updated. The development of our backports
for CentOS has moved over to the
[Hyperscale SIG](https://wiki.centos.org/SpecialInterestGroup/Hyperscale),
where packages that directly replace a base package (e.g. `systemd`) are still
being actively maintained and released. Packages that are missing in CentOS
altogether (e.g. `mkosi`) are instead being developed as part of
[Fedora EPEL](https://fedoraproject.org/wiki/EPEL).

The following table tracks where each package is currently being maintained.

| Package                            | Where                                                                                     |
| ---------------------------------- | ----------------------------------------------------------------------------------------- |
| dbus-broker                        | [EPEL 8](https://src.fedoraproject.org/rpms/dbus-broker/tree/epel8)                       |
| dbus                               | [CentOS Stream 8](https://git.centos.org/rpms/dbus/tree/c8s)                              |
| dcrpm                              | [EPEL 8](https://src.fedoraproject.org/rpms/python-dcrpm/tree/epel8)                      |
| initscripts                        | [CentOS Stream 8](https://git.centos.org/rpms/initscripts/tree/c8s)                       |
| libbpf                             | [CentOS Stream 8](https://git.centos.org/rpms/libbpf/tree/c8s)                            |
| meson                              | [Hyperscale SIG](https://git.centos.org/rpms/meson/tree/c8s-sig-hyperscale)               |
| mkosi                              | [EPEL 8](https://src.fedoraproject.org/rpms/mkosi/tree/epel8)                             |
| ninja-build                        | [Hyperscale SIG](https://git.centos.org/rpms/ninja-build/tree/c8s-sig-hyperscale)         |
| python3-dnf-flunk-dependent-remove | [EPEL 8](https://src.fedoraproject.org/rpms/dnf-plugin-flunk_dependent_remove/tree/epel8) |
| python34-cssselect                 | [EPEL 8](https://src.fedoraproject.org/rpms/python-cssselect/tree/epel8)                  |
| python34-lxml                      | [CentOS Stream 8](https://git.centos.org/rpms/python-lxml/tree/c8s)                       |
| systemd-compat-libs                | [retired](https://github.com/facebookincubator/systemd-compat-libs/pull/10)               |
| systemd                            | [Hyperscale SIG](https://git.centos.org/rpms/systemd/tree/c8s-sig-hyperscale)             |
| util-linux                         | [CentOS Stream 8](https://git.centos.org/rpms/util-linux/tree/c8s)                        |
