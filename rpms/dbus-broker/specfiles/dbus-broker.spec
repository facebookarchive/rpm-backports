%global dbus_user_id 81

Name:                 dbus-broker
Version:              21
Release:              6%{?dist}
Summary:              Linux D-Bus Message Broker
License:              ASL 2.0
URL:                  https://github.com/bus1/dbus-broker
Source0:              https://github.com/bus1/dbus-broker/releases/download/v%{version}/dbus-broker-%{version}.tar.xz
Patch0:               0001-units-system-add-messagebus-alias.patch
Patch1:               0001-launch-improve-error-handling-for-opendir.patch
Patch2:               0001-metrics-change-the-constant-used-for-invalid-timesta.patch
Patch3:               0001-dbus-socket-treat-MSG_CTRUNC-gracefully.patch
Provides:             bundled(c-dvar) = 1
Provides:             bundled(c-ini) = 1
Provides:             bundled(c-list) = 3
Provides:             bundled(c-rbtree) = 3
Provides:             bundled(c-shquote) = 1
%{?systemd_requires}
BuildRequires:        pkgconfig(audit)
BuildRequires:        pkgconfig(expat)
BuildRequires:        pkgconfig(dbus-1)
BuildRequires:        pkgconfig(libcap-ng)
BuildRequires:        pkgconfig(libselinux)
BuildRequires:        pkgconfig(libsystemd)
BuildRequires:        pkgconfig(systemd)
BuildRequires:        gcc
BuildRequires:        glibc-devel
BuildRequires:        meson
BuildRequires:        python3-docutils
Requires:             dbus-common
Requires(pre):        shadow-utils
Requires(post):       /usr/bin/systemctl
# for triggerpostun
Requires:             /usr/bin/systemctl

%description
dbus-broker is an implementation of a message bus as defined by the D-Bus
specification. Its aim is to provide high performance and reliability, while
keeping compatibility to the D-Bus reference implementation. It is exclusively
written for Linux systems, and makes use of many modern features provided by
recent Linux kernel releases.

%prep
%autosetup -p1

%build
%meson -Dselinux=true -Daudit=true -Ddocs=true -Dsystem-console-users=gdm
%meson_build

%install
%meson_install

%check
%meson_test

%pre
# create dbus user and group
getent group dbus >/dev/null || groupadd -f -g %{dbus_user_id} -r dbus
if ! getent passwd dbus >/dev/null ; then
    if ! getent passwd %{dbus_user_id} >/dev/null ; then
      useradd -r -u %{dbus_user_id} -g %{dbus_user_id} -d '/' -s /sbin/nologin -c "System message bus" dbus
    else
      useradd -r -g %{dbus_user_id} -d '/' -s /sbin/nologin -c "System message bus" dbus
    fi
fi
exit 0

%post
# Since F30 dbus-broker is the default bus implementation. However, changing
# the systemd presets does not automatically switch over. Instead, we have to
# explicitly disable dbus-daemon and enable dbus-broker. We do this on the first
# install of this package.
#
# Note that there is a virtual circular dependency between this package and the
# fedora presets (in 'fedora-release'). To break this, we explicitly enable
# dbus-broker here. Once the presets are in, we will be able to drop the
# explicit 'enable' calls and rely on the presets below.
#systemd_post dbus-broker.service
#systemd_user_post dbus-broker.service
#
# systemd has special checks if dbus.socket and dbus.service are active and
# will close the dbus connection if they are not. When the symlinks are changed
# from dbus-daemon to dbus-broker, systemd would think that dbus is gone,
# because dbus.service (which now is an alias for dbus-broker.service) is not
# active. Let's add a temporary override that will keep pid1 happy.

if [ $1 -eq 1 ] ; then
        if systemctl is-enabled -q dbus-daemon.service; then
                # Install a temporary generator that'll keep providing the
                # alias as it was.
                mkdir -p /run/systemd/system-generators/
                cat >>/run/systemd/system-generators/dbus-symlink-generator <<EOF
#!/bin/sh
ln -s /usr/lib/systemd/system/dbus-daemon.service \$2/dbus.service
EOF
                chmod +x /run/systemd/system-generators/dbus-symlink-generator
                chcon system_u:object_r:init_exec_t:s0 /run/systemd/system-generators/dbus-symlink-generator || :
        fi

        if systemctl is-enabled -q --global dbus-daemon.service; then
                mkdir -p /run/systemd/user-generators/
                cat >>/run/systemd/user-generators/dbus-symlink-generator <<EOF
#!/bin/sh
ln -s /usr/lib/systemd/user/dbus-daemon.service \$2/dbus.service
EOF
                chmod +x /run/systemd/user-generators/dbus-symlink-generator
        fi

        systemctl --no-reload -q          disable dbus-daemon.service || :
        systemctl --no-reload -q --global disable dbus-daemon.service || :
        systemctl --no-reload -q          enable dbus-broker.service || :
        systemctl --no-reload -q --global enable dbus-broker.service || :
fi

%journal_catalog_update

%preun
%systemd_preun dbus-broker.service
%systemd_user_preun dbus-broker.service

%postun
%systemd_postun dbus-broker.service
%systemd_user_postun dbus-broker.service

%triggerpostun -- dbus-daemon
if [ $2 -eq 0 ] ; then
        # See above comment about presets.
        #systemctl --no-reload preset dbus-broker.service || :
        #systemctl --no-reload --global preset dbus-broker.service || :
        systemctl --no-reload          enable dbus-broker.service || :
        systemctl --no-reload --global enable dbus-broker.service || :
fi

%files
%license AUTHORS
%license LICENSE
%{_bindir}/dbus-broker
%{_bindir}/dbus-broker-launch
%{_journalcatalogdir}/dbus-broker.catalog
%{_journalcatalogdir}/dbus-broker-launch.catalog
%{_mandir}/man1/dbus-broker.1*
%{_mandir}/man1/dbus-broker-launch.1*
%{_unitdir}/dbus-broker.service
%{_userunitdir}/dbus-broker.service

%changelog
* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Neal Gompa <ngompa13@gmail.com> - 21-5
- Fix reference to dbus_user_id macro in scriptlet

* Wed Jul 10 2019 Jonathan Brielmaier <jbrielmaier@suse.de> - 21-4
- Make creation of dbus user/group more robust, fixes #1717925

* Thu May  9 2019 Tom Gundersen <teg@jklm.no> - 21-2
- Gracefully handle missing FDs in received messages, #1706883
- Minor bugfixes

* Fri May  3 2019 Tom Gundersen <teg@jklm.no> - 21-1
- Don't fail on EACCESS when reading config, fixes #1704920

* Thu May  2 2019 Tom Gundersen <teg@jklm.no> - 21-1
- Minor bugfixes related to config reload for #1704488

* Wed Apr 17 2019 Tom Gundersen <teg@jklm.no> - 20-4
- Fix assert due to failing reload #1700514

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 20-3
- Rebuild with Meson fix for #1699099

* Thu Apr 11 2019 Tom Gundersen <teg@jklm.no> - 20-2
- Fix the c_assert macro

* Wed Apr 10 2019 Tom Gundersen <teg@jklm.no> - 20-1
- Improve handling of broken or deprecated configuration
- Avoid at_console workaround if possible

* Tue Apr  9 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 19-2
- Add a temporary generator to fix switching from dbus-daemon to
  dbus-broker (#1674045)

* Thu Mar 28 2019 Tom Gundersen <teg@jklm.no> - 19-1
- Minor bug fixes

* Thu Feb 21 2019 Tom Gundersen <teg@jklm.no> - 18-1
- Minor bug fixes

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Tom Gundersen <teg@jklm.no> - 17-3
- run in the root network namespace

* Sat Jan 12 2019 Tom Gundersen <teg@jklm.no> - 17-2
- ignore config files that cannot be opened (fix rhbz #1665450)

* Wed Jan 2 2019 Tom Gundersen <teg@jklm.no> - 17-1
- apply more sandboxing through systemd
- improve logging on disconnect
- don't send FDs to clients who don't declare support

* Wed Nov 28 2018 Tom Gundersen <teg@jklm.no> - 16-8
- don't apply presets on updates to dbus-daemon

* Mon Nov 26 2018 Tom Gundersen <teg@jklm.no> - 16-7
- enable service file correctly at install

* Mon Nov 26 2018 Tom Gundersen <teg@jklm.no> - 16-5
- use full paths when calling binaries from rpm scripts

* Sun Nov 25 2018 Tom Gundersen <teg@jklm.no> - 16-4
- fix SELinux bug

* Tue Oct 30 2018 Tom Gundersen <teg@jklm.no> - 16-3
- add explicit systemctl dependency

* Tue Oct 23 2018 David Herrmann <dh.herrmann@gmail.com> - 16-2
- create dbus user and group if non-existant
- add explicit %%postlets to switch over to the broker as default

* Fri Oct 12 2018 Tom Gundersen <teg@jklm.no> - 16-1
- make resource limits configurable
- rerun presets in case dbus-daemon is disabled

* Thu Aug 30 2018 Tom Gundersen <teg@jklm.no> - 15-4
- depend on dbus-common rather than dbus

* Wed Aug 29 2018 Tom Gundersen <teg@jklm.no> - 15-3
- run %%systemd_user rpm macros

* Mon Aug 27 2018 Tom Gundersen <teg@jklm.no> - 15-2
- add back --verbose switch for backwards compatibility

* Wed Aug 08 2018 Tom Gundersen <teg@jklm.no> - 15-1
- fix audit support
- make logging about invalid config less verbose

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Tom Gundersen <teg@jklm.no> - 14-1
- use inotify to reload config automatically
- run as the right user
- new compatibility features, bugfixes and performance enhancements

* Mon Apr 23 2018 Tom Gundersen <teg@jklm.no> - 13-1
- Namespace transient systemd units per launcher instance
- Reduce reliance on NSS
- Fix deadlock with nss-systemd

* Wed Feb 21 2018 Tom Gundersen <teg@jklm.no> - 11-1
- The 'gdm' user is now considered at_console=true
- Bugfixes and performance enhancements

* Wed Feb 07 2018 Tom Gundersen <teg@jklm.no> - 10-1
- Bugfixes and performance enhancements

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Tom Gundersen <teg@jklm.no> - 9-1
- Avoid nss deadlock at start-up
- Support ExecReload
- Respect User= in service files

* Tue Oct 17 2017 Tom Gundersen <teg@jklm.no> - 8-1
- Dont clean-up children of activated services by default
- Dont use audit from the user instance
- Support the ReloadConfig() API

* Tue Oct 17 2017 Tom Gundersen <teg@jklm.no> - 7-1
- Upstream bugfix release

* Mon Oct 16 2017 Tom Gundersen <teg@jklm.no> - 6-1
- Upstream bugfix release

* Tue Oct 10 2017 Tom Gundersen <teg@jklm.no> - 5-1
- Drop downstream SELinux module
- Support (in a limited way) at_console= policies
- Order dbus-broker before basic.target

* Fri Sep 08 2017 Tom Gundersen <teg@jklm.no> - 4-1
- Use audit for SELinux logging
- Support full search-paths for service files
- Log policy failures

* Fri Aug 18 2017 Tom Gundersen <teg@jklm.no> - 3-1
- Add manpages

* Wed Aug 16 2017 Tom Gundersen <teg@jklm.no> - 2-2
- Add license to package

* Wed Aug 16 2017 Tom Gundersen <teg@jklm.no> - 2-1
- Add SELinux support

* Sun Aug 13 2017 Tom Gundersen <teg@jklm.no> - 1-1
- Initial RPM release

