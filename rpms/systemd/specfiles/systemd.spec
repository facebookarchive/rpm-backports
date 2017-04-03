# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

%global pkgdir %{_prefix}/lib/systemd
%global system_unit_dir %{pkgdir}/system

%global _pkgdocdir %{_docdir}/systemd

Name:           systemd
Url:            http://www.freedesktop.org/wiki/Software/systemd
Version:        231
Release:        11.fb1
# For a breakdown of the licensing, see README
License:        LGPLv2+ and MIT and GPLv2+
Summary:        A System and Service Manager

# download tarballs with "spectool -g systemd.spec"
%if %{defined gitcommit}
Source0:        https://github.com/systemd/systemd/archive/%{?gitcommit}.tar.gz#/%{name}-%{gitcommitshort}.tar.gz
%else
Source0:        https://github.com/systemd/systemd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
# This file must be available before %%prep.
# It is generated during systemd build and can be found in src/core/.
Source1:        triggers.systemd

# Prevent accidental removal of the systemd package
Source4:        yum-protect-systemd.conf

Source7:        systemd-journal-remote.xml
Source8:        systemd-journal-gatewayd.xml
Source9:        20-yama-ptrace.conf
Source10:       systemd-udev-trigger-no-reload.conf

BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  pam-devel
BuildRequires:  libselinux-devel
BuildRequires:  audit-libs-devel
BuildRequires:  cryptsetup-devel
BuildRequires:  dbus-devel
BuildRequires:  libacl-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libblkid-devel
BuildRequires:  xz-devel
BuildRequires:  lz4-devel
BuildRequires:  bzip2-devel
BuildRequires:  libidn-devel
BuildRequires:  libcurl-devel
BuildRequires:  kmod-devel
BuildRequires:  elfutils-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  gnutls-devel
BuildRequires:  qrencode-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  iptables-devel
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  pkgconfig
BuildRequires:  intltool
BuildRequires:  gperf
BuildRequires:  gawk
BuildRequires:  tree
BuildRequires:  python34-devel
BuildRequires:  python34-lxml
%ifarch %{ix86} x86_64 aarch64
BuildRequires:  gnu-efi gnu-efi-devel
%endif
BuildRequires:  libseccomp-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

Requires(post): coreutils
Requires(post): sed
Requires(post): acl
Requires(post): grep
Requires(pre):  coreutils
Requires(pre):  /usr/bin/getent
Requires(pre):  /usr/sbin/groupadd
Requires:       dbus
Requires:       %{name}-pam = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Recommends:     diffutils
Requires:       util-linux
Recommends:     libxkbcommon%{?_isa}
Provides:       /bin/systemctl
Provides:       /sbin/shutdown
Provides:       syslog
Provides:       systemd-units = %{version}-%{release}
Obsoletes:      system-setup-keyboard < 0.9
Provides:       system-setup-keyboard = 0.9
# systemd-sysv-convert was removed in f20: https://fedorahosted.org/fpc/ticket/308
Obsoletes:      systemd-sysv < 206
# self-obsoletes so that dnf will install new subpackages on upgrade (#1260394)
Obsoletes:      %{name} < 229-5
Obsoletes:      systemd-stubs
Provides:       systemd-sysv = 206
%if 0%{?fedora}
Conflicts:      fedora-release < 23-0.12
%endif

Patch0: systemctl--be-sure-to-be-quiet-with--systemctl-is-enabled---quiet----3819-.patch
Patch1: logind--0--and-100--should-be-valid-for-UserTasksMax---3836-.patch
Patch2: systemd-ask-password--make-sure-directory-watch-is-started-before-cryptsetup---3850-.patch
Patch3: Revert--logind--really-handle--KeyIgnoreInhibited-options-in-logind-conf-.patch
Patch4: man--explain-that--KeyIgnoreInhibited-only-apply-to-a-subset-of-locks.patch
Patch5: systemctl--fix-preset-all-with-missing--etc-systemd-system.patch
Patch6: shared-install--remove-unused-paramater-and-add-more-comments.patch
Patch7: shared-install--ignore-unit-symlinks-when-doing-preset-all.patch
Patch8: man--describe-what-symlinks-to-unit-do--and-specify-that-presets-must-use-real-names.patch
Patch9: shared-install--move-root-skipping-into-create_symlink--.patch
Patch10: shared-install--when-creating-symlinks--keep-existing-relative-symlinks.patch
Patch11: shared-install--properly-report-masked-units-listed-in-Also-.patch
Patch12: Revert--pid1--reconnect-to-the-console-before-being-re-executed-.patch
Patch13: systemd--ignore-lack-of-tty-when-checking-whether-colors-should-be-enabled.patch
Patch14: shared-install--do-not-enable-masked-instances---4005-.patch
Patch15: If-the-notification-message-length-is-0--ignore-the-message---4237-.patch
Patch16: pid1--don-t-return-any-error-in-manager_dispatch_notify_fd-----4240-.patch
Patch17: pid1--process-zero-length-notification-messages-again.patch
Patch18: shared-install--fix-set-default-with-empty-root---4118-.patch
Patch19: virt--add-possibility-to-skip-the-check-for-chroot---4374-.patch
Patch20: resolved--create--etc-resolv-conf-symlink-at-runtime.patch
Patch21: kernel-install--add-fedora-specific-callouts-to-new-kernel-pkg.patch
Patch22: FB--add-back-compat-libs.patch
Patch23: FB--Add-FusionIO-device--dev-fio-persistent-storage-udev-rule.patch
Patch24: build-sys--conditionally-disable-LTO-if-requested---3823-.patch
Patch25: tests--don-t-run-private-device-tests-if-running-in-a-container.patch
Patch26: tests--don-t-test-hostname-if-it-looks-like-an-id128.patch
Patch27: tests--skip-process-1-tests-if-systemd-not-is-running.patch
Patch28: tests--skip-udev-test-if-running-inside-a-chroot.patch
Patch29: logind--update-empty-and--infinity--handling-for--User-TasksMax---3835-.patch
Patch30: core--add-cgroup-CPU-controller-support-on-the-unified-hierarchy.patch
Patch31: core--no-assert-during-runtime-if-start-command-vanishes.patch
















%description
systemd is a system and service manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic.

%package libs
Summary:        systemd libraries
License:        LGPLv2+ and MIT
Obsoletes:      libudev < 183
Obsoletes:      systemd < 185-4
Conflicts:      systemd < 185-4
Obsoletes:      nss-myhostname < 0.4
Provides:       nss-myhostname = 0.4

%description libs
Libraries for systemd and udev.

%package compat-libs
Summary:        systemd compatibility libraries
License:        LGPLv2+ and MIT
# To reduce confusion, this package can only be installed in parallel
# with the normal systemd-libs, same version.
Requires:       systemd-libs%{?_isa} = %{version}-%{release}

%description compat-libs
Compatibility libraries for systemd. If your package requires this
package, you need to update your link options and build.

%package pam
Summary:        systemd PAM module
Requires:       %{name} = %{version}-%{release}

%description pam
Systemd PAM module registers the session with systemd-logind.

%package devel
Summary:        Development headers for systemd
License:        LGPLv2+ and MIT
# We need both libsystemd and libsystemd-<compat> libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-compat-libs%{?_isa} = %{version}-%{release}
Provides:       libudev-devel = %{version}
Obsoletes:      libudev-devel < 183

%description devel
Development headers and auxiliary files for developing applications linking
to libudev or libsystemd.

%package udev
Summary: Rule-based device node and kernel event manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post): grep
Requires:       kmod >= 18-4
# obsolete parent package so that dnf will install new subpackage on upgrade (#1260394)
Obsoletes:      %{name} < 229-5
Provides:       udev = %{version}
Obsoletes:      udev < 183
# https://bugzilla.redhat.com/show_bug.cgi?id=1377733#c9
Recommends:     systemd-bootchart
License:        LGPLv2+

%description udev
This package contains systemd-udev and the rules and hardware database
needed to manage device nodes. This package is necessary on physical
machines and in virtual machines, but not in containers.

%package container
# Name is the same as in Debian
Summary: Tools for containers and VMs
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
# obsolete parent package so that dnf will install new subpackage on upgrade (#1260394)
Obsoletes:      %{name} < 229-5
License:        LGPLv2+

%description container
Systemd tools to spawn and manage containers and virtual machines.

This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package journal-remote
# Name is the same as in Debian
Summary:        Tools to send journal events over the network
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        LGPLv2+
Requires(pre):    /usr/bin/getent
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Provides:       %{name}-journal-gateway = %{version}-%{release}
Obsoletes:      %{name}-journal-gateway < 227-7

%description journal-remote
Programs to forward journal entries over the network, using encrypted HTTP,
and to write journal files from serialized journal contents.

This package contains systemd-journal-gatewayd,
systemd-journal-remote, and systemd-journal-upload.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1































%build
./autogen.sh

%{?fedora: %global ntpvendor fedora}
%{?rhel:   %global ntpvendor rhel}
%{!?ntpvendor: echo 'NTP vendor zone is not set!'; exit 1}

CONFIGURE_OPTS=(
        --libexecdir=%{_prefix}/lib
        --with-sysvinit-path=/etc/rc.d/init.d
        --with-rc-local-script-path-start=/etc/rc.d/rc.local
        --with-ntp-servers='0.%{ntpvendor}.pool.ntp.org 1.%{ntpvendor}.pool.ntp.org 2.%{ntpvendor}.pool.ntp.org 3.%{ntpvendor}.pool.ntp.org'
        --without-kill-user-processes
        --disable-lto
)

%if 0%{?facebook}
CONFIGURE_OPTS+=(
        --with-ntp-servers='1.ntp.vip.facebook.com 2.ntp.vip.facebook.com 3.ntp.vip.facebook.com 4.ntp.vip.facebook.com'
        --with-dns-servers='10.127.255.51 10.191.255.51 2401:db00:eef0:a53:: 2401:db00:eef0:b53::'
)
%endif

%configure \
        "${CONFIGURE_OPTS[@]}" \
        --enable-compat-libs \
        --enable-xkbcommon \
        PYTHON=%{__python3}
make %{?_smp_mflags} GCC_COLORS="" V=1

%install
%make_install

find %{buildroot} \( -name '*.a' -o -name '*.la' \) -delete

# remove .so file for the shared library, it's not supposed to be used
rm %{buildroot}%{pkgdir}/libsystemd-shared.so

# udev links
mkdir -p %{buildroot}/%{_sbindir}
ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
ln -s ../lib/systemd/systemd %{buildroot}%{_sbindir}/init
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/reboot
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/halt
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/poweroff
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/shutdown
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/telinit
ln -s ../bin/systemctl %{buildroot}%{_sbindir}/runlevel

# Compatiblity and documentation files
touch %{buildroot}/etc/crypttab
chmod 600 %{buildroot}/etc/crypttab

ln -s ../sysctl.conf %{buildroot}/etc/sysctl.d/99-sysctl.conf

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the user deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/systemd/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{system_unit_dir}/basic.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/default.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/dbus.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/syslog.target.wants
mkdir -p %{buildroot}%{_localstatedir}/run
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/run/utmp
touch %{buildroot}%{_localstatedir}/log/{w,b}tmp

# Make sure the user generators dir exists too
mkdir -p %{buildroot}%{pkgdir}/system-generators
mkdir -p %{buildroot}%{pkgdir}/user-generators

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/localtime
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf

# Make sure the shutdown/sleep drop-in dirs exist
mkdir -p %{buildroot}%{pkgdir}/system-shutdown/
mkdir -p %{buildroot}%{pkgdir}/system-sleep/

# Make sure directories in /var exist
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/coredump
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/backlight
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/rfkill
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/journal-upload
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/linger
mkdir -p %{buildroot}%{_localstatedir}/log/journal
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed
touch %{buildroot}%{_localstatedir}/lib/systemd/clock

# Install yum protection fragment
install -Dm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/yum/protected.d/systemd.conf

# Install additional docs
# https://bugzilla.redhat.com/show_bug.cgi?id=1234951
install -Dm0644 -t %{buildroot}%{_pkgdocdir}/ %{SOURCE9}

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
mkdir -p %{buildroot}%{system_unit_dir}/systemd-udev-trigger.service.d/
install -Dm0644 -t %{buildroot}%{system_unit_dir}/systemd-udev-trigger.service.d/ %{SOURCE10}

%find_lang %{name}

%check
make check VERBOSE=1 || { cat test-suite.log; exit 1; }

# Check for botched translations (https://bugzilla.redhat.com/show_bug.cgi?id=1226566)
test -z "$(grep -L xml:lang %{buildroot}%{_datadir}/polkit-1/actions/org.freedesktop.*.policy)"

#############################################################################################

%include %{SOURCE1}

%pre
getent group cdrom >/dev/null 2>&1 || groupadd -r -g 11 cdrom >/dev/null 2>&1 || :
getent group utmp >/dev/null 2>&1 || groupadd -r -g 22 utmp >/dev/null 2>&1 || :
getent group tape >/dev/null 2>&1 || groupadd -r -g 33 tape >/dev/null 2>&1 || :
getent group dialout >/dev/null 2>&1 || groupadd -r -g 18 dialout >/dev/null 2>&1 || :
getent group input >/dev/null 2>&1 || groupadd -r input >/dev/null 2>&1 || :
getent group systemd-journal >/dev/null 2>&1 || groupadd -r -g 190 systemd-journal 2>&1 || :
getent group systemd-timesync >/dev/null 2>&1 || groupadd -r systemd-timesync 2>&1 || :
getent passwd systemd-timesync >/dev/null 2>&1 || useradd -r -l -g systemd-timesync -d / -s /sbin/nologin -c "systemd Time Synchronization" systemd-timesync >/dev/null 2>&1 || :
getent group systemd-network >/dev/null 2>&1 || groupadd -r -g 192 systemd-network 2>&1 || :
getent passwd systemd-network >/dev/null 2>&1 || useradd -r -u 192 -l -g systemd-network -d / -s /sbin/nologin -c "systemd Network Management" systemd-network >/dev/null 2>&1 || :
getent group systemd-resolve >/dev/null 2>&1 || groupadd -r -g 193 systemd-resolve 2>&1 || :
getent passwd systemd-resolve >/dev/null 2>&1 || useradd -r -u 193 -l -g systemd-resolve -d / -s /sbin/nologin -c "systemd Resolver" systemd-resolve >/dev/null 2>&1 || :

%post
systemd-machine-id-setup >/dev/null 2>&1 || :
systemctl daemon-reexec >/dev/null 2>&1 || :
journalctl --update-catalog >/dev/null 2>&1 || :
systemd-tmpfiles --create >/dev/null 2>&1 || :

if [ $1 -eq 1 ] ; then
     # create /var/log/journal only on initial installation
     mkdir -p %{_localstatedir}/log/journal
fi

# Make sure new journal files will be owned by the "systemd-journal" group
chgrp systemd-journal /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2> /dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :
chmod g+s /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2> /dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :

# Apply ACL to the journal directory
setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/ >/dev/null 2>&1 || :

# Stop-gap until rsyslog.rpm does this on its own. (This is supposed
# to fail when the link already exists)
ln -s /usr/lib/systemd/system/rsyslog.service /etc/systemd/system/syslog.service >/dev/null 2>&1 || :

# Remove spurious /etc/fstab entries from very old installations
# https://bugzilla.redhat.com/show_bug.cgi?id=1009023
if [ -e /etc/fstab ]; then
   grep -v -E -q '^(devpts|tmpfs|sysfs|proc)' /etc/fstab || \
         sed -i.rpm.bak -r '/^devpts\s+\/dev\/pts\s+devpts\s+defaults\s+/d; /^tmpfs\s+\/dev\/shm\s+tmpfs\s+defaults\s+/d; /^sysfs\s+\/sys\s+sysfs\s+defaults\s+/d; /^proc\s+\/proc\s+proc\s+defaults\s+/d' /etc/fstab || :
fi

# Services we install by default, and which are controlled by presets.
if [ $1 -eq 1 ] ; then
        systemctl preset \
                remote-fs.target \
                getty@.service \
                serial-getty@.service \
                console-getty.service \
                console-shell.service \
                debug-shell.service \
                systemd-networkd.service \
                systemd-networkd-wait-online.service \
                systemd-resolved.service \
                >/dev/null 2>&1 || :
fi

# remove obsolete systemd-readahead file
rm -f /.readahead > /dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ] ; then
        systemctl disable \
                remote-fs.target \
                getty@.service \
                serial-getty@.service \
                console-getty.service \
                console-shell.service \
                debug-shell.service \
                systemd-readahead-replay.service \
                systemd-readahead-collect.service \
                systemd-networkd.service \
                systemd-networkd-wait-online.service \
                systemd-resolved.service \
                >/dev/null 2>&1 || :

        rm -f /etc/systemd/system/default.target >/dev/null 2>&1 || :
fi

%post libs
/sbin/ldconfig

# sed-fu to add myhostanme to hosts line and remove mymachines
# from passwd and group lines of /etc/nsswitch.conf
# https://bugzilla.redhat.com/show_bug.cgi?id=1284325
# https://meetbot.fedoraproject.org/fedora-meeting/2015-11-25/fesco.2015-11-25-18.00.html
# To avoid the removal, e.g. add a space at the end of the line.
if [ -f /etc/nsswitch.conf ] ; then
        grep -v -E -q '^hosts:.* myhostname' /etc/nsswitch.conf &&
        sed -i.bak -e '
                /^hosts:/ !b
                /\<myhostname\>/ b
                s/[[:blank:]]*$/ myhostname/
                ' /etc/nsswitch.conf >/dev/null 2>&1 || :

        grep -E -q '^(passwd|group):.* mymachines$' /etc/nsswitch.conf &&
        sed -i.bak -r -e '
                s/^(passwd:.*) mymachines$/\1/;
                s/^(group:.*) mymachines$/\1/;
                ' /etc/nsswitch.conf >/dev/null 2>&1 || :
fi

%postun libs -p /sbin/ldconfig

%global udev_services systemd-udev{d,-settle,-trigger}.service systemd-udevd-{control,kernel}.socket systemd-timesyncd.service

%post udev
# Move old stuff around in /var/lib
mv %{_localstatedir}/lib/random-seed %{_localstatedir}/lib/systemd/random-seed &>/dev/null
mv %{_localstatedir}/lib/backlight %{_localstatedir}/lib/systemd/backlight &>/dev/null

udevadm hwdb --update >/dev/null 2>&1
%systemd_post %udev_services
/usr/lib/systemd/systemd-random-seed save 2>&1

# Replace obsolete keymaps
# https://bugzilla.redhat.com/show_bug.cgi?id=1151958
grep -q -E '^KEYMAP="?fi-latin[19]"?' /etc/vconsole.conf 2>/dev/null &&
    sed -i.rpm.bak -r 's/^KEYMAP="?fi-latin[19]"?/KEYMAP="fi"/' /etc/vconsole.conf

exit 0

%preun udev
%systemd_preun %udev_services

%postun udev
# Only restart systemd-udev, to run the upgraded dameon.
# Others are either oneshot services, or sockets, and restarting them causes issues (#1378974)
%systemd_postun_with_restart systemd-udevd.service

%pre journal-remote
getent group systemd-journal-gateway >/dev/null 2>&1 || groupadd -r -g 191 systemd-journal-gateway 2>&1 || :
getent passwd systemd-journal-gateway >/dev/null 2>&1 || useradd -r -l -u 191 -g systemd-journal-gateway -d %{_localstatedir}/log/journal -s /sbin/nologin -c "Journal Gateway" systemd-journal-gateway >/dev/null 2>&1 || :
getent group systemd-journal-remote >/dev/null 2>&1 || groupadd -r systemd-journal-remote 2>&1 || :
getent passwd systemd-journal-remote >/dev/null 2>&1 || useradd -r -l -g systemd-journal-remote -d %{_localstatedir}/log/journal/remote -s /sbin/nologin -c "Journal Remote" systemd-journal-remote >/dev/null 2>&1 || :
getent group systemd-journal-upload >/dev/null 2>&1 || groupadd -r systemd-journal-upload 2>&1 || :
getent passwd systemd-journal-upload >/dev/null 2>&1 || useradd -r -l -g systemd-journal-upload -G systemd-journal -d %{_localstatedir}/log/journal/upload -s /sbin/nologin -c "Journal Upload" systemd-journal-upload >/dev/null 2>&1 || :

%post journal-remote
%systemd_post systemd-journal-gatewayd.socket systemd-journal-gatewayd.service
%systemd_post systemd-journal-remote.socket systemd-journal-remote.service
%systemd_post systemd-journal-upload.service

%preun journal-remote
%systemd_preun systemd-journal-gatewayd.socket systemd-journal-gatewayd.service
%systemd_preun systemd-journal-remote.socket systemd-journal-remote.service
%systemd_preun systemd-journal-upload.service

%postun journal-remote
%systemd_postun_with_restart systemd-journal-gatewayd.service
%systemd_postun_with_restart systemd-journal-remote.service
%systemd_postun_with_restart systemd-journal-upload.service

%global _docdir_fmt %{name}

%files -f %{name}.lang
%doc %{_pkgdocdir}
%exclude %{_pkgdocdir}/LICENSE.*
%license LICENSE.GPL2 LICENSE.LGPL2.1
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/network
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/crypttab
%{_sysconfdir}/sysctl.d/99-sysctl.conf
%dir %{pkgdir}
%{pkgdir}/system-generators
%exclude %{pkgdir}/system-generators/systemd-cryptsetup-generator
%exclude %{pkgdir}/system-generators/systemd-gpt-auto-generator
%exclude %{pkgdir}/system-generators/systemd-hibernate-resume-generator
%{pkgdir}/user-generators
%dir %{pkgdir}/system-shutdown
%dir %{pkgdir}/system-sleep
%dir %{pkgdir}/catalog
%dir %{pkgdir}/network
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_prefix}/lib/sysusers.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.d
%dir %{_datadir}/systemd
%dir %{_datadir}/pkgconfig
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%ghost %dir %{_localstatedir}/log/journal
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
%ghost %dir %{_localstatedir}/lib/systemd/coredump
%ghost %dir %{_localstatedir}/lib/systemd/backlight
%ghost %dir %{_localstatedir}/lib/systemd/rfkill
%ghost %dir %{_localstatedir}/lib/systemd/linger
%ghost %{_localstatedir}/lib/systemd/random-seed
%ghost %{_localstatedir}/lib/systemd/clock
%ghost %{_localstatedir}/lib/systemd/catalog/database
%{_localstatedir}/log/README
%ghost %attr(0664,root,utmp) %{_localstatedir}/run/utmp
%ghost %attr(0664,root,utmp) %{_localstatedir}/log/wtmp
%ghost %attr(0600,root,utmp) %{_localstatedir}/log/btmp
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.network1.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/yum/protected.d/systemd.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
%{_rpmconfigdir}/macros.d/macros.systemd
%{_sysconfdir}/xdg/systemd
%{_sysconfdir}/rc.d/init.d/README
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/localtime
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%dir %{_sysconfdir}/X11/xorg.conf.d
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%{_bindir}/systemctl
%{_bindir}/systemd-notify
%{_bindir}/systemd-analyze
%{_bindir}/systemd-escape
%{_bindir}/systemd-ask-password
%{_bindir}/systemd-tty-ask-password-agent
%{_bindir}/systemd-machine-id-setup
%{_bindir}/loginctl
%{_bindir}/journalctl
%{_bindir}/busctl
%{_bindir}/networkctl
%{_bindir}/coredumpctl
%{_bindir}/systemd-tmpfiles
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgls
%{_bindir}/systemd-cgtop
%{_bindir}/systemd-delta
%{_bindir}/systemd-run
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-inhibit
%{_bindir}/systemd-path
%{_bindir}/systemd-resolve
%{_bindir}/systemd-sysusers
%{_bindir}/systemd-firstboot
%{_bindir}/systemd-socket-activate
%{_bindir}/hostnamectl
%{_bindir}/localectl
%{_bindir}/timedatectl
%{pkgdir}/systemd
%{pkgdir}/libsystemd-shared-%{version}.so
%{system_unit_dir}
%{pkgdir}/user
%{pkgdir}/resolv.conf
%exclude %{system_unit_dir}/*udev*
%exclude %{system_unit_dir}/*/*udev*
%exclude %{system_unit_dir}/*hwdb*
%exclude %{system_unit_dir}/*/*hwdb*
%exclude %{system_unit_dir}/systemd-vconsole-setup.service
%exclude %{system_unit_dir}/*/systemd-vconsole-setup.service
%exclude %{system_unit_dir}/kmod-static-nodes.service
%exclude %{system_unit_dir}/*/kmod-static-nodes.service
%exclude %{system_unit_dir}/systemd-tmpfiles-setup-dev.service
%exclude %{system_unit_dir}/*/systemd-tmpfiles-setup-dev.service
%exclude %{system_unit_dir}/*.machine1.*
%exclude %{system_unit_dir}/*/*.machine1.*
%exclude %{system_unit_dir}/*.import1.*
%exclude %{system_unit_dir}/*/*.import1.*
%exclude %{system_unit_dir}/systemd-machined.service
%exclude %{system_unit_dir}/systemd-importd.service
%exclude %{system_unit_dir}/machine.slice
%exclude %{system_unit_dir}/machines.target
%exclude %{system_unit_dir}/var-lib-machines.mount
%exclude %{system_unit_dir}/*/var-lib-machines.mount
%exclude %{system_unit_dir}/systemd-journal-gatewayd.*
%exclude %{system_unit_dir}/systemd-journal-remote.*
%exclude %{system_unit_dir}/systemd-journal-upload.*
%exclude %{system_unit_dir}/systemd-rfkill.*
%exclude %{system_unit_dir}/systemd-backlight*
%exclude %{system_unit_dir}/*/systemd-random-seed.service
%exclude %{system_unit_dir}/systemd-random-seed.service
%exclude %{system_unit_dir}/systemd-quotacheck.service
%exclude %{system_unit_dir}/quotaon.service
%exclude %{system_unit_dir}/*/systemd-modules-load.service
%exclude %{system_unit_dir}/systemd-modules-load.service
%exclude %{system_unit_dir}/systemd-timesyncd.service
%exclude %{system_unit_dir}/systemd-hibernate-resume@.service
%exclude %{system_unit_dir}/systemd-hibernate.service
%exclude %{system_unit_dir}/systemd-suspend.service
%exclude %{system_unit_dir}/systemd-hybrid-sleep.service
%exclude %{system_unit_dir}/systemd-nspawn@.service
%exclude %{pkgdir}/systemd-udevd
%exclude %{pkgdir}/systemd-vconsole-setup
%exclude %{pkgdir}/systemd-machined
%exclude %{pkgdir}/systemd-import
%exclude %{pkgdir}/systemd-importd
%exclude %{pkgdir}/systemd-pull
%exclude %{pkgdir}/systemd-journal-gatewayd
%exclude %{pkgdir}/systemd-journal-remote
%exclude %{pkgdir}/systemd-journal-upload
%exclude %{pkgdir}/systemd-backlight
%exclude %{pkgdir}/systemd-rfkill
%exclude %{pkgdir}/systemd-random-seed
%exclude %{pkgdir}/systemd-quotacheck
%exclude %{pkgdir}/systemd-modules-load
%exclude %{pkgdir}/systemd-timesyncd
%exclude %{pkgdir}/systemd-cryptsetup
%exclude %{pkgdir}/systemd-hibernate-resume
%exclude %{pkgdir}/systemd-sleep

%{pkgdir}/systemd-*
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%{_prefix}/lib/tmpfiles.d/x11.conf
%{_prefix}/lib/tmpfiles.d/legacy.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/etc.conf
%{_prefix}/lib/tmpfiles.d/home.conf
%{_prefix}/lib/tmpfiles.d/journal-nocow.conf
%{_prefix}/lib/sysctl.d/50-default.conf
%{_prefix}/lib/sysctl.d/50-coredump.conf
%{_prefix}/lib/sysusers.d/basic.conf
%{_prefix}/lib/sysusers.d/systemd.conf
%{pkgdir}/system-preset/90-systemd.preset
%{pkgdir}/catalog/systemd.catalog
%{_prefix}/lib/kernel/install.d/50-depmod.install
%{_prefix}/lib/kernel/install.d/90-loaderentry.install
%{_sbindir}/init
%{_sbindir}/reboot
%{_sbindir}/halt
%{_sbindir}/poweroff
%{_sbindir}/shutdown
%{_sbindir}/telinit
%{_sbindir}/runlevel
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%exclude %{_mandir}/man*/*udev*
%exclude %{_mandir}/man*/*hwdb*
%exclude %{_mandir}/man*/systemd-tmpfiles-setup-dev.service*
%exclude %{_mandir}/man*/systemd-journal-gateway*
%exclude %{_mandir}/man*/*journal-remote.*
%exclude %{_mandir}/man*/*modules-load.*
%exclude %{_mandir}/man*/*timesyncd.*
%exclude %{_mandir}/man*/systemd-hibernate*
%exclude %{_mandir}/man*/systemd-hybrid-sleep*
%exclude %{_mandir}/man*/systemd-suspend*
%exclude %{_mandir}/man*/systemd-nspawn.*
%exclude %{_mandir}/man*/systemd-vconsole-setup*
%exclude %{_mandir}/man*/systemd-machined*
%exclude %{_mandir}/man*/systemd-journal-remote*
%exclude %{_mandir}/man*/systemd-journal-upload*
%exclude %{_mandir}/man*/systemd-backlight*
%exclude %{_mandir}/man*/systemd-rfkill*
%exclude %{_mandir}/man*/systemd-random-seed*
%exclude %{_mandir}/man*/systemd-quotacheck*
%exclude %{_mandir}/man*/systemd-cryptsetup*
%exclude %{_mandir}/man*/systemd-sleep*

%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/systemd/kbd-model-map
%{_datadir}/systemd/language-fallback-map
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc
%{_datadir}/bash-completion/completions/*
%exclude %{_datadir}/bash-completion/completions/udevadm
%exclude %{_datadir}/bash-completion/completions/machinectl
%exclude %{_datadir}/bash-completion/completions/systemd-nspawn
%{_datadir}/zsh/site-functions/*
%exclude %{_datadir}/zsh/site-functions/_udevadm
%exclude %{_datadir}/zsh/site-functions/_machinectl
%exclude %{_datadir}/zsh/site-functions/_systemd-nspawn
%{pkgdir}/catalog/systemd.*.catalog
%{pkgdir}/network/80-container-host0.network

%ghost %dir %{_localstatedir}/lib/rpm-state/systemd

%files libs
%{_libdir}/libnss_myhostname.so.2
%{_libdir}/libnss_resolve.so.2
%{_libdir}/libudev.so.*
%{_libdir}/libsystemd.so.*
%license LICENSE.LGPL2.1

%files compat-libs
%{_libdir}/libsystemd-daemon.so.*
%{_libdir}/libsystemd-login.so.*
%{_libdir}/libsystemd-journal.so.*
%{_libdir}/libsystemd-id128.so.*

%files pam
%{_libdir}/security/pam_systemd.so

%files devel
%dir %{_includedir}/systemd
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_libdir}/libsystemd-daemon.so
%{_libdir}/libsystemd-login.so
%{_libdir}/libsystemd-journal.so
%{_libdir}/libsystemd-id128.so
%{_includedir}/systemd/sd-daemon.h
%{_includedir}/systemd/sd-login.h
%{_includedir}/systemd/sd-journal.h
%{_includedir}/systemd/sd-id128.h
%{_includedir}/systemd/sd-messages.h
%{_includedir}/systemd/sd-bus-protocol.h
%{_includedir}/systemd/sd-bus-vtable.h
%{_includedir}/systemd/sd-bus.h
%{_includedir}/systemd/sd-event.h
%{_includedir}/systemd/_sd-common.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_libdir}/pkgconfig/libsystemd-daemon.pc
%{_libdir}/pkgconfig/libsystemd-login.pc
%{_libdir}/pkgconfig/libsystemd-journal.pc
%{_libdir}/pkgconfig/libsystemd-id128.pc
%{_mandir}/man3/*

%files udev
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/hwdb.d
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%ghost %{_sysconfdir}/udev/hwdb.bin
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%{system_unit_dir}/*udev*
%{system_unit_dir}/*/*udev*
%{system_unit_dir}/*hwdb*
%{system_unit_dir}/*/*hwdb*
%{system_unit_dir}/systemd-vconsole-setup.service
%{system_unit_dir}/*/systemd-vconsole-setup.service
%{system_unit_dir}/kmod-static-nodes.service
%{system_unit_dir}/*/kmod-static-nodes.service
%{system_unit_dir}/systemd-tmpfiles-setup-dev.service
%{system_unit_dir}/*/systemd-tmpfiles-setup-dev.service
%{system_unit_dir}/systemd-rfkill.*
%{system_unit_dir}/systemd-backlight*
%{system_unit_dir}/*/systemd-random-seed.service
%{system_unit_dir}/systemd-random-seed.service
%{system_unit_dir}/systemd-quotacheck.service
%{system_unit_dir}/quotaon.service
%{system_unit_dir}/*/systemd-modules-load.service
%{system_unit_dir}/systemd-modules-load.service
%{system_unit_dir}/systemd-timesyncd.service
%{system_unit_dir}/systemd-hibernate-resume@.service
%{system_unit_dir}/systemd-hibernate.service
%{system_unit_dir}/systemd-hybrid-sleep.service
%{system_unit_dir}/systemd-suspend.service
%{_bindir}/udevadm
%{_sbindir}/udevadm
%{_bindir}/systemd-hwdb
%{_bindir}/bootctl
%{_bindir}/kernel-install
%{pkgdir}/systemd-udevd
%{pkgdir}/systemd-vconsole-setup
%{pkgdir}/systemd-backlight
%{pkgdir}/systemd-rfkill
%{pkgdir}/systemd-random-seed
%{pkgdir}/systemd-quotacheck
%{pkgdir}/systemd-modules-load
%{pkgdir}/systemd-timesyncd
%{pkgdir}/systemd-cryptsetup
%{pkgdir}/systemd-hibernate-resume
%{pkgdir}/systemd-sleep

%{pkgdir}/network/99-default.link
%{_prefix}/lib/udev
%{_datadir}/bash-completion/completions/udevadm
%{_datadir}/zsh/site-functions/_udevadm
%{pkgdir}/system-generators/systemd-cryptsetup-generator
%{pkgdir}/system-generators/systemd-gpt-auto-generator
%{pkgdir}/system-generators/systemd-hibernate-resume-generator
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf

%ifarch %{ix86} x86_64 aarch64
%dir %{pkgdir}/boot
%dir %{pkgdir}/boot/efi
%{pkgdir}/boot/efi/*.efi
%{pkgdir}/boot/efi/*.stub
%endif

%{_mandir}/man[1578]/*udev*
%{_mandir}/man[1578]/*hwdb*
%{_mandir}/man[1578]/systemd-tmpfiles-setup-dev.service*
%{_mandir}/man[1578]/*modules-load.*
%{_mandir}/man[1578]/*timesyncd.*
%{_mandir}/man[1578]/systemd-hibernate*
%{_mandir}/man[1578]/systemd-suspend*
%{_mandir}/man[1578]/systemd-vconsole-setup*
%{_mandir}/man[1578]/systemd-backlight*
%{_mandir}/man[1578]/systemd-rfkill*
%{_mandir}/man[1578]/systemd-random-seed*
%{_mandir}/man[1578]/systemd-quotacheck*
%{_mandir}/man[1578]/systemd-cryptsetup*
%{_mandir}/man[1578]/systemd-sleep*

%files container
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.import1.conf
%{_libdir}/libnss_mymachines.so.2
%{_bindir}/machinectl
%{_bindir}/systemd-nspawn
%{pkgdir}/import-pubring.gpg
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{system_unit_dir}/*.machine1.*
%{system_unit_dir}/*/*.machine1.*
%{system_unit_dir}/*.import1.*
%{system_unit_dir}/*/*.import1.*
%{system_unit_dir}/systemd-machined.service
%{system_unit_dir}/systemd-importd.service
%{system_unit_dir}/machine.slice
%{system_unit_dir}/machines.target
%{system_unit_dir}/var-lib-machines.mount
%{system_unit_dir}/*/var-lib-machines.mount
%{system_unit_dir}/systemd-nspawn@.service
%{pkgdir}/systemd-machined
%{pkgdir}/systemd-import
%{pkgdir}/systemd-importd
%{pkgdir}/systemd-pull
%{pkgdir}/network/80-container-ve.network
%{pkgdir}/network/80-container-vz.network
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.import1.service
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy
%{_datadir}/bash-completion/completions/machinectl
%{_datadir}/bash-completion/completions/systemd-nspawn
%{_datadir}/zsh/site-functions/_machinectl
%{_datadir}/zsh/site-functions/_systemd-nspawn
%{_mandir}/man1/machinectl.*
%{_mandir}/man8/systemd-machined.*
%{_mandir}/man8/*mymachines.*

%files journal-remote
%config(noreplace) %{_sysconfdir}/systemd/journal-remote.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%{system_unit_dir}/systemd-journal-gatewayd.*
%{system_unit_dir}/systemd-journal-remote.*
%{system_unit_dir}/systemd-journal-upload.*
%{pkgdir}/systemd-journal-gatewayd
%{pkgdir}/systemd-journal-remote
%{pkgdir}/systemd-journal-upload
%{_prefix}/lib/tmpfiles.d/systemd-remote.conf
%{_prefix}/lib/sysusers.d/systemd-remote.conf
%dir %attr(0644,systemd-journal-upload,systemd-journal-upload) %{_localstatedir}/lib/systemd/journal-upload
%{_datadir}/systemd/gatewayd
%{_mandir}/man[1578]/*journal-remote.*
%{_mandir}/man[1578]/systemd-journal-upload*
%{_mandir}/man[1578]/systemd-journal-gateway*
%{_mandir}/man[1578]/systemd-nspawn.*

%changelog
* Mon Apr  3 2017 Davide Cavalca <dcavalca@fb.com> - 231-11.fb1
- use facebook macro to gate Facebook-specific settings
- rebuild against new RPM backport
- update patches

* Tue Mar 14 2017 Patrick White <pwhite@fb.com> - 231-2.fb4
- add poettering patch to fix hitting an assert (PR#4447)

* Tue Oct 18 2016 Jan Synáček <jsynacek@redhat.com> - 231-11
- SPC - Cannot restart host operating from container (#1384523)

* Sun Oct  9 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-10
- Do not recreate /var/log/journal on upgrades (#1383066)
- Move nss-myhostname provides to systemd-libs (#1383271)

* Fri Oct  7 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-9
- Fix systemctl set-default (#1374371)
- Prevent systemd-udev-trigger.service from restarting (follow-up for #1378974)

* Tue Oct  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-8
- Apply fix for #1378974

* Mon Oct  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-7
- Apply patches properly

* Thu Sep 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-6
- Better fix for (#1380286)

* Thu Sep 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-5
- Denial-of-service bug against pid1 (#1380286)

* Thu Aug 25 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-4
- Fix preset-all (#1363858)
- Fix issue with daemon-reload messing up graphics (#1367766)
- A few other bugfixes

* Wed Aug 10 2016 Davide Cavalca <dcavalca@fb.com> - 231-2.fb3
- add mpawlowski root filesystem namespace patch for #12621017
- add htejun patch for cgroup2 cpu controller (PR#3905)
- update htejun logind patch from PR#3835

* Wed Aug 03 2016 Adam Williamson <awilliam@redhat.com> - 231-3
- Revert preset-all change, it broke stuff (#1363858)

* Thu Jul 28 2016 Davide Cavalca <dcavalca@fb.com> - 231-2.fb2
- add /dev/fio patch from bwann for GH#3718
- import PR#3821 updates and rebase patches on github
- add htejun logind patch for UserTasksMax (#12460186, PR#3835)

* Wed Jul 27 2016 Davide Cavalca <dcavalca@fb.com> - 231-2.fb1
- Facebook rebuild
- Fix test failures in mock (#7950934, PR#3821)
- drop fsck on root patch now that we have the new dracut (see PR#3822)
- Rework LTO disable patch to be conditional (#11565880, PR#3823)
- update compat-libs and rebase onto public branch 
  (https://github.com/davide125/systemd/tree/compat-libs)
- add back python support now that we have python34-lxml
- add back xkbcommon support as it's available in rolling os updates

* Wed Jul 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-2
- Call preset-all on initial installation (#1118740)
- Fix botched Recommends for libxkbcommon

* Tue Jul 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-1
- Update to latest version

* Tue Jul 19 2016 Davide Cavalca <dcavalca@fb.com> - 230-2.fb2
- fix fsck for root filesystem on firstboot after install (#11352467)

* Wed Jun  8 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 230-3
- Update to latest git snapshot (fixes for systemctl set-default,
  polkit lingering policy, reversal of the framebuffer rules,
  unaligned access fixes, fix for StartupBlockIOWeight-over-dbus).
  Those changes are interspersed with other changes and new features
  (mostly in lldp, networkd, and nspawn). Some of those new features
  might not work, but I think that existing functionality should not
  be broken, so it seems worthwile to update to the snapshot.

* Thu May 26 2016 Davide Cavalca <dcavalca@fb.com> - 230-2.fb1
- Facebook rebuild
- backport htejun PRs for cgroup2 (#3337, #3329, #3315, #3417, #3418)
- add back compat-libs

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-2
- Remove systemd-compat-libs on upgrade

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-1
- New version
- Drop compat-libs
- Require libxkbcommon explictly, since the automatic dependency will
  not be generated anymore

* Thu May 12 2016 Tejun Heo <htejun@fb.com> - 229-1.fb6
- backport https://github.com/systemd/systemd/pull/3246 to fix slice overrides

* Mon May 09 2016 Davide Cavalca <dcavalca@fb.com> - 229-1.fb5
- update Tejun Heo patches for cgroup2 io controller support

* Fri Apr 29 2016 Davide Cavalca <dcavalca@fb.com> - 229-1.fb4
- add Tejun Heo test patch for cgroup2 IO controllers support (#10638181)

* Tue Apr 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 229-15
- Remove duplicated entries in -container %%files (#1330395)

* Fri Apr 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-14
- Move installation of udev services to udev subpackage (#1329023)

* Mon Apr 18 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-13
- Split out systemd-pam subpackage (#1327402)

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-12
- move more binaries and services from the main package to subpackages

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-11
- move more binaries and services from the main package to subpackages

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-10
- move device dependant stuff to the udev subpackage

* Thu Mar 24 2016 Davide Cavalca <dcavalca@fb.com> - 229-1.fb3
- add Tejun Heo patches for cgroups v2 support (#10268183)

* Tue Mar 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-9
- Add myhostname to /etc/nsswitch.conf (#1318303)

* Mon Mar 21 2016 Harald Hoyer <harald@redhat.com> - 229-8
- fixed kernel-install for copying files for grubby
Resolves: rhbz#1299019

* Thu Mar 17 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-7
- Moar patches (#1316964, #1317928)
- Move vconsole-setup and tmpfiles-setup-dev bits to systemd-udev
- Protect systemd-udev from deinstallation

* Fri Mar 11 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-6
- Create /etc/resolv.conf symlink from systemd-resolved (#1313085)

* Fri Mar  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-5
- Split out systemd-container subpackage (#1163412)
- Split out system-udev subpackage
- Add various bugfix patches, incl. a tentative fix for #1308771

* Wed Mar 02 2016 Davide Cavalca <dcavalca@fb.com> - 229-1.fb2
- revert RPM trigger macros for #10119506

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 229-4
- Power64 and s390(x) now have libseccomp support
- aarch64 has gnu-efi

* Tue Feb 23 2016 Jan Synáček <jsynacek@redhat.com> - 229-3
- Fix build failures on ppc64 (#1310800)

* Tue Feb 16 2016 Dennis Gilmore <dennis@ausil.us> - 229-2
- revert: fixed kernel-install for copying files for grubby
Resolves: rhbz#1299019
- this causes the dtb files to not get installed at all and the fdtdir
- line in extlinux.conf to not get updated correctly

* Tue Feb 16 2016 Davide Cavalca <dcavalca@fb.com> - 229-1.fb1
- Facebook rebuilt
- disable LTO to fix a build segfault with LTO

* Thu Feb 11 2016 Michal Sekletar <msekleta@redhat.com> - 229-1
- New upstream release

* Thu Feb 11 2016 Harald Hoyer <harald@redhat.com> - 228-10.gite35a787
- fixed kernel-install for copying files for grubby
Resolves: rhbz#1299019

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 228-9.gite35a787
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 228-8.gite35a787
- Rebuild for binutils on aarch64 fix

* Fri Jan 08 2016 Dan Horák <dan[at]danny.cz> - 228-7.gite35a787
- apply the conflict with fedora-release only in Fedora

* Thu Dec 10 2015 Jan Synáček <jsynacek@redhat.com> - 228-6.gite35a787
- Fix rawhide build failures on ppc64 (#1286249)

* Sun Nov 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-6.gite35a787
- Create /etc/systemd/network (#1286397)

* Thu Nov 26 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-5.gite35a787
- Do not install nss modules by default

* Tue Nov 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-4.gite35a787
- Update to latest upstream git: there is a bunch of fixes
  (nss-mymachines overflow bug, networkd fixes, more completions are
  properly installed), mixed with some new resolved features.
- Rework file triggers so that they always run before daemons are restarted

* Mon Nov 23 2015 Davide Cavalca <dcavalca@fb.com> - 228-3.fb1
- Facebook rebuilt
- disable test-namespace
- revert rpm file triggers as they don't work on el7

* Thu Nov 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-3
- Enable rpm file triggers for daemon-reload

* Thu Nov 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-2
- Fix version number in obsoleted package name (#1283452)

* Wed Nov 18 2015 Kay Sievers <kay@redhat.com> - 228-1
- New upstream release

* Thu Nov 12 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 227-7
- Rename journal-gateway subpackage to journal-remote
- Ignore the access mode on /var/log/journal (#1048424)
- Do not assume fstab is present (#1281606)

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 227-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 227-5
- Rebuild for libmicrohttpd soname bump

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 227-4
- Rebuilt for Python3.5 rebuild

* Wed Nov  4 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 227-3
- Fix syntax in kernel-install (#1277264)

* Tue Nov 03 2015 Michal Schmidt <mschmidt@redhat.com> - 227-2
- Rebuild for libmicrohttpd soname bump.

* Fri Oct 09 2015 Davide Cavalca <dcavalca@fb.com> - 227-1.fb1
- disable tests broken on centos6
- fix build with centos7 curl
- kernel-install: add fedora specific callouts to new-kernel-pkg

* Wed Oct  7 2015 Kay Sievers <kay@redhat.com> - 227-1
- New upstream release

* Fri Sep 18 2015 Jan Synáček <jsynacek@redhat.com> - 226-3
- user systemd-journal-upload should be in systemd-journal group (#1262743)

* Fri Sep 18 2015 Kay Sievers <kay@redhat.com> - 226-2
- Add selinux to  system-user PAM config

* Tue Sep  8 2015 Kay Sievers <kay@redhat.com> - 226-1
- New upstream release

* Thu Aug 27 2015 Kay Sievers <kay@redhat.com> - 225-1
- New upstream release

* Fri Jul 31 2015 Kay Sievers <kay@redhat.com> - 224-1
- New upstream release

* Wed Jul 29 2015 Kay Sievers <kay@redhat.com> - 223-2
- update to git snapshot

* Wed Jul 29 2015 Kay Sievers <kay@redhat.com> - 223-1
- New upstream release

* Thu Jul  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 222-2
- Remove python subpackages (python-systemd in now standalone)

* Tue Jul  7 2015 Kay Sievers <kay@redhat.com> - 222-1
- New upstream release

* Mon Jul  6 2015 Kay Sievers <kay@redhat.com> - 221-5.git619b80a
- update to git snapshot

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 221-4.git604f02a
- Add example file with yama config (#1234951)

* Sun Jul 5 2015 Kay Sievers <kay@redhat.com> - 221-3.git604f02a
- update to git snapshot

* Mon Jun 22 2015 Kay Sievers <kay@redhat.com> - 221-2
- build systemd-boot EFI tools

* Fri Jun 19 2015 Lennart Poettering <lpoetter@redhat.com> - 221-1
- New upstream release
- Undoes botched translation check, should be reinstated later?

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 220-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 220-9
- The gold linker is now fixed on aarch64

* Tue Jun  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 220-8
- Remove gudev which is now provided as separate package (libgudev)
- Fix for spurious selinux denials (#1224211)
- Udev change events (#1225905)
- Patches for some potential crashes
- ProtectSystem=yes does not touch /home
- Man page fixes, hwdb updates, shell completion updates
- Restored persistent device symlinks for bcache, xen block devices
- Tag all DRM cards as master-of-seat

* Tue Jun 09 2015 Harald Hoyer <harald@redhat.com> 220-7
- fix udev block device watch

* Tue Jun 09 2015 Harald Hoyer <harald@redhat.com> 220-6
- add support for network disk encryption

* Sun Jun  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 220-5
- Disable gold on aarch64 until it's fixed (tracked in rhbz #1225156)

* Sat May 30 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 220-4
- systemd-devel should require systemd-libs, not the main package (#1226301)
- Check for botched translations (#1226566)
- Make /etc/udev/hwdb.d part of the rpm (#1226379)

* Thu May 28 2015 Richard W.M. Jones <rjones@redhat.com> - 220-3
- Add patch to fix udev --daemon not cleaning child processes
  (upstream commit 86c3bece38bcf5).

* Wed May 27 2015 Richard W.M. Jones <rjones@redhat.com> - 220-2
- Add patch to fix udev --daemon crash (upstream commit 040e689654ef08).

* Thu May 21 2015 Lennart Poettering <lpoetter@redhat.com> - 220-1
- New upstream release
- Drop /etc/mtab hack, as that's apparently fixed in mock now (#1116158)
- Remove ghosting for %%{_sysconfdir}/systemd/system/runlevel*.target, these targets are not configurable anymore in systemd upstream
- Drop work-around for #1002806, since this is solved upstream now

* Wed May 20 2015 Dennis Gilmore <dennis@ausil.us> - 219-15
- fix up the conflicts version for fedora-release

* Wed May 20 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-14
- Remove presets (#1221340)
- Fix (potential) crash and memory leak in timedated, locking failure
  in systemd-nspawn, crash in resolved.
- journalctl --list-boots should be faster
- zsh completions are improved
- various ommissions in docs are corrected (#1147651)
- VARIANT and VARIANT_ID fields in os-release are documented
- systemd-fsck-root.service is generated in the initramfs (#1201979, #1107818)
- systemd-tmpfiles should behave better on read-only file systems (#1207083)

* Wed Apr 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-13
- Patches for some outstanding annoyances
- Small keyboard hwdb updates

* Wed Apr  8 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-12
- Tighten requirements between subpackages (#1207381).

* Sun Mar 22 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-11
- Move all parts systemd-journal-{remote,upload} to
  systemd-journal-gatewayd subpackage (#1193143).
- Create /var/lib/systemd/journal-upload directory (#1193145).
- Cut out lots of stupid messages at debug level which were obscuring more
  important stuff.
- Apply "tentative" state for devices only when they are added, not removed.
- Ignore invalid swap pri= settings (#1204336)
- Fix SELinux check for timedated operations to enable/disable ntp (#1014315)
- Fix comparing of filesystem paths (#1184016)

* Sat Mar 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-10
- Fixes for bugs 1186018, 1195294, 1185604, 1196452.
- Hardware database update.
- Documentation fixes.
- A fix for journalctl performance regression.
- Fix detection of inability to open files in journalctl.
- Detect SuperH architecture properly.
- The first of duplicate lines in tmpfiles wins again.
- Do vconsole setup after loading vconsole driver, not fbcon.
- Fix problem where some units were restarted during systemd reexec.
- Fix race in udevadm settle tripping up NetworkManager.
- Downgrade various log messages.
- Fix issue where journal-remote would process some messages with a delay.
- GPT /srv partition autodiscovery is fixed.
- Reconfigure old Finnish keymaps in post (#1151958)

* Tue Mar 10 2015 Jan Synáček <jsynacek@redhat.com> - 219-9
- Buttons on Lenovo X6* tablets broken (#1198939)

* Tue Mar  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-8
- Reworked device handling (#1195761)
- ACL handling fixes (with a script in %%post)
- Various log messages downgraded (#1184712)
- Allow PIE on s390 again (#1197721)

* Wed Feb 25 2015 Michal Schmidt <mschmidt@redhat.com> - 219-7
- arm: reenable lto. gcc-5.0.0-0.16 fixed the crash (#1193212)

* Tue Feb 24 2015 Colin Walters <walters@redhat.com> - 219-6
- Revert patch that breaks Atomic/OSTree (#1195761)

* Fri Feb 20 2015 Michal Schmidt <mschmidt@redhat.com> - 219-5
- Undo the resolv.conf workaround, Aim for a proper fix in Rawhide.

* Fri Feb 20 2015 Michal Schmidt <mschmidt@redhat.com> - 219-4
- Revive fedora-disable-resolv.conf-symlink.patch to unbreak composes.

* Wed Feb 18 2015 Michal Schmidt <mschmidt@redhat.com> - 219-3
- arm: disabling gold did not help; disable lto instead (#1193212)

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 219-2
- Update 90-default.present for dbxtool.

* Mon Feb 16 2015 Lennart Poettering <lpoetter@redhat.com> - 219-1
- New upstream release
- This removes the sysctl/bridge hack, a different solution needs to be found for this (see #634736)
- This removes the /etc/resolv.conf hack, anaconda needs to fix their handling of /etc/resolv.conf as symlink
- This enables "%%check"
- disable gold on arm, as that is broken (see #1193212)

* Mon Feb 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 218-6
- aarch64 now has seccomp support

* Thu Feb 05 2015 Michal Schmidt <mschmidt@redhat.com> - 218-5
- Don't overwrite systemd.macros with unrelated Source file.

* Thu Feb  5 2015 Jan Synáček <jsynacek@redhat.com> - 218-4
- Add a touchpad hwdb (#1189319)

* Thu Jan 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 218-4
- Enable xkbcommon dependency to allow checking of keymaps
- Fix permissions of /var/log/journal (#1048424)
- Enable timedatex in presets (#1187072)
- Disable rpcbind in presets (#1099595)

* Wed Jan  7 2015 Jan Synáček <jsynacek@redhat.com> - 218-3
- RFE: journal: automatically rotate the file if it is unlinked (#1171719)

* Mon Jan 05 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 218-3
- Add firewall description files (#1176626)

* Thu Dec 18 2014 Jan Synáček <jsynacek@redhat.com> - 218-2
- systemd-nspawn doesn't work on s390/s390x (#1175394)

* Wed Dec 10 2014 Lennart Poettering <lpoetter@redhat.com> - 218-1
- New upstream release
- Enable "nss-mymachines" in /etc/nsswitch.conf

* Thu Nov 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 217-4
- Change libgudev1 to only require systemd-libs (#727499), there's
  no need to require full systemd stack.
- Fixes for bugs #1159448, #1152220, #1158035.
- Bash completions updates to allow propose more units for start/restart,
  and completions for set-default,get-default.
- Again allow systemctl enable of instances.
- Hardware database update and fixes.
- Udev crash on invalid options and kernel commandline timeout parsing are fixed.
- Add "embedded" chassis type.
- Sync before 'reboot -f'.
- Fix restarting of timer units.

* Wed Nov 05 2014 Michal Schmidt <mschmidt@redhat.com> - 217-3
- Fix hanging journal flush (#1159641)

* Fri Oct 31 2014 Michal Schmidt <mschmidt@redhat.com> - 217-2
- Fix ordering cycles involving systemd-journal-flush.service and
  remote-fs.target (#1159117)

* Tue Oct 28 2014 Lennart Poettering <lpoetter@redhat.com> - 217-1
- New upstream release

* Fri Oct 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-12
- Drop PackageKit.service from presets (#1154126)

* Mon Oct 13 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-11
- Conflict with old versions of initscripts (#1152183)
- Remove obsolete Finnish keymap (#1151958)

* Fri Oct 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-10
- Fix a problem with voluntary daemon exits and some other bugs
  (#1150477, #1095962, #1150289)

* Fri Oct 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-9
- Update to latest git, but without the readahead removal patch
  (#1114786, #634736)

* Wed Oct 01 2014 Kay Sievers <kay@redhat.com> - 216-8
- revert "don't reset selinux context during CHANGE events"

* Wed Oct 01 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 216-7
- add temporary workaround for #1147910
- don't reset selinux context during CHANGE events

* Wed Sep 10 2014 Michal Schmidt <mschmidt@redhat.com> - 216-6
- Update timesyncd with patches to avoid hitting NTP pool too often.

* Tue Sep 09 2014 Michal Schmidt <mschmidt@redhat.com> - 216-5
- Use common CONFIGURE_OPTS for build2 and build3.
- Configure timesyncd with NTP servers from Fedora/RHEL vendor zone.

* Wed Sep 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-4
- Move config files for sd-j-remote/upload to sd-journal-gateway subpackage (#1136580)

* Thu Aug 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 216-3
- Drop no LTO build option for aarch64/s390 now it's fixed in binutils (RHBZ 1091611)

* Thu Aug 21 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-2
- Re-add patch to disable resolve.conf symlink (#1043119)

* Wed Aug 20 2014 Lennart Poettering <lpoetter@redhat.com> - 216-1
- New upstream release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 215-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Dan Horák <dan[at]danny.cz> 215-11
- disable LTO also on s390(x)

* Sat Aug 09 2014 Harald Hoyer <harald@redhat.com> 215-10
- fixed PPC64LE

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> - 215-9
- fix license handling

* Wed Jul 30 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-8
- Create systemd-journal-remote and systemd-journal-upload users (#1118907)

* Thu Jul 24 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-7
- Split out systemd-compat-libs subpackage

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 215-6
- Rebuilt for gobject-introspection 1.41.4

* Mon Jul 21 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-5
- Fix SELinux context of /etc/passwd-, /etc/group-, /etc/.updated (#1121806)
- Add missing BR so gnutls and elfutils are used

* Sat Jul 19 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-4
- Various man page updates
- Static device node logic is conditionalized on CAP_SYS_MODULES instead of CAP_MKNOD
  for better behaviour in containers
- Some small networkd link handling fixes
- vconsole-setup runs setfont before loadkeys (https://bugs.freedesktop.org/show_bug.cgi?id=80685)
- New systemd-escape tool
- XZ compression settings are tweaked to greatly improve journald performance
- "watch" is accepted as chassis type
- Various sysusers fixes, most importantly correct selinux labels
- systemd-timesyncd bug fix (https://bugs.freedesktop.org/show_bug.cgi?id=80932)
- Shell completion improvements
- New udev tag ID_SOFTWARE_RADIO can be used to instruct logind to allow user access
- XEN and s390 virtualization is properly detected

* Mon Jul 07 2014 Colin Walters <walters@redhat.com> - 215-3
- Add patch to disable resolve.conf symlink (#1043119)

* Sun Jul 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-2
- Move systemd-journal-remote to systemd-journal-gateway package (#1114688)
- Disable /etc/mtab handling temporarily (#1116158)

* Thu Jul 03 2014 Lennart Poettering <lpoetter@redhat.com> - 215-1
- New upstream release
- Enable coredump logic (which abrt would normally override)

* Sun Jun 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 214-5
- On aarch64 disable LTO as it still has issues on that arch

* Thu Jun 26 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-4
- Bugfixes (#996133, #1112908)

* Mon Jun 23 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-3
- Actually create input group (#1054549)

* Sun Jun 22 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-2
- Do not restart systemd-logind on upgrades (#1110697)
- Add some patches (#1081429, #1054549, #1108568, #928962)

* Wed Jun 11 2014 Lennart Poettering <lpoetter@redhat.com> - 214-1
- New upstream release
- Get rid of "floppy" group, since udev uses "disk" now
- Reenable LTO

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kay Sievers <kay@redhat.com> - 213-3
- fix systemd-timesync user creation

* Wed May 28 2014 Michal Sekletar <msekleta@redhat.com> - 213-2
- Create temporary files after installation (#1101983)
- Add sysstat-collect.timer, sysstat-summary.timer to preset policy (#1101621)

* Wed May 28 2014 Kay Sievers <kay@redhat.com> - 213-1
- New upstream release

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 212-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 23 2014 Adam Williamson <awilliam@redhat.com> - 212-5
- revert change from 212-4, causes boot fail on single CPU boxes (RHBZ 1095891)

* Wed May 07 2014 Kay Sievers <kay@redhat.com> - 212-4
- add netns udev workaround

* Wed May 07 2014 Michal Sekletar <msekleta@redhat.com> - 212-3
- enable uuidd.socket by default (#1095353)

* Sat Apr 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 212-2
- Disable building with -flto for the moment due to gcc 4.9 issues (RHBZ 1091611)

* Tue Mar 25 2014 Lennart Poettering <lpoetter@redhat.com> - 212-1
- New upstream release

* Mon Mar 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 211-2
- Explicitly define which upstream platforms support libseccomp

* Tue Mar 11 2014 Lennart Poettering <lpoetter@redhat.com> - 211-1
- New upstream release

* Mon Mar 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-8
- Fix logind unpriviledged reboot issue and a few other minor fixes
- Limit generator execution time
- Recognize buttonless joystick types

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 210-7
- ppc64le needs link warnings disabled, too

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 210-6
- move ifarch ppc64le to correct place (libseccomp req)

* Fri Mar 07 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-5
- Bugfixes: #1047568, #1047039, #1071128, #1073402
- Bash completions for more systemd tools
- Bluetooth database update
- Manpage fixes

* Thu Mar 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-4
- Apply work-around for ppc64le too (#1073647).

* Sat Mar 01 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-3
- Backport a few patches, add completion for systemd-nspawn.

* Fri Feb 28 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-3
- Apply work-arounds for ppc/ppc64 for bugs 1071278 and 1071284

* Mon Feb 24 2014 Lennart Poettering <lpoetter@redhat.com> - 210-2
- Check more services against preset list and enable by default

* Mon Feb 24 2014 Lennart Poettering <lpoetter@redhat.com> - 210-1
- new upstream release

* Sun Feb 23 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 209-2.gitf01de96
- Enable dnssec-triggerd.service by default (#1060754)

* Sun Feb 23 2014 Kay Sievers <kay@redhat.com> - 209-2.gitf01de96
- git snapshot to sort out ARM build issues

* Thu Feb 20 2014 Lennart Poettering <lpoetter@redhat.com> - 209-1
- new upstream release

* Tue Feb 18 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-15
- Make gpsd lazily activated (#1066421)

* Mon Feb 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-14
- Back out patch which causes user manager to be destroyed when unneeded
  and spams logs (#1053315)

* Sun Feb 16 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-13
- A different fix for #1023820 taken from Mageia
- Backported fix for #997031
- Hardward database updates, man pages improvements, a few small memory
  leaks, utf-8 correctness and completion fixes
- Support for key-slot option in crypttab

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 208-12
- Own the %%{_prefix}/lib/kernel(/*) and %%{_datadir}/zsh(/*) dirs.

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-11
- Backport a few fixes, relevant documentation updates, and HWDB changes
  (#1051797, #1051768, #1047335, #1047304, #1047186, #1045849, #1043304,
   #1043212, #1039351, #1031325, #1023820, #1017509, #953077)
- Flip journalctl to --full by default (#984758)

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-9
- Apply two patches for #1026860

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-8
- Bump release to stay ahead of f20

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-7
- Backport patches (#1023041, #1036845, #1006386?)
- HWDB update
- Some small new features: nspawn --drop-capability=, running PID 1 under
  valgrind, "yearly" and "annually" in calendar specifications
- Some small documentation and logging updates

* Tue Nov 19 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-6
- Bump release to stay ahead of f20

* Tue Nov 19 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-5
- Use unit name in PrivateTmp= directories (#957439)
- Update manual pages, completion scripts, and hardware database
- Configurable Timeouts/Restarts default values
- Support printing of timestamps on the console
- Fix some corner cases in detecting when writing to the console is safe
- Python API: convert keyword values to string, fix sd_is_booted() wrapper
- Do not tread missing /sbin/fsck.btrfs as an error (#1015467)
- Allow masking of fsck units
- Advertise hibernation to swap files
- Fix SO_REUSEPORT settings
- Prefer converted xkb keymaps to legacy keymaps (#981805, #1026872)
- Make use of newer kmod
- Assorted bugfixes: #1017161, #967521, #988883, #1027478, #821723, #1014303

* Tue Oct 22 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-4
- Add temporary fix for #1002806

* Mon Oct 21 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-3
- Backport a bunch of fixes and hwdb updates

* Wed Oct 2 2013 Lennart Poettering <lpoetter@redhat.com> - 208-2
- Move old random seed and backlight files into the right place

* Wed Oct 2 2013 Lennart Poettering <lpoetter@redhat.com> - 208-1
- New upstream release

* Thu Sep 26 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 207-5
- Do not create /var/var/... dirs

* Wed Sep 18 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 207-4
- Fix policykit authentication
- Resolves: rhbz#1006680

* Tue Sep 17 2013 Harald Hoyer <harald@redhat.com> 207-3
- fixed login
- Resolves: rhbz#1005233

* Mon Sep 16 2013 Harald Hoyer <harald@redhat.com> 207-2
- add some upstream fixes for 207
- fixed swap activation
- Resolves: rhbz#1008604

* Fri Sep 13 2013 Lennart Poettering <lpoetter@redhat.com> - 207-1
- New upstream release

* Fri Sep 06 2013 Harald Hoyer <harald@redhat.com> 206-11
- support "debug" kernel command line parameter
- journald: fix fd leak in journal_file_empty
- journald: fix vacuuming of archived journals
- libudev: enumerate - do not try to match against an empty subsystem
- cgtop: fixup the online help
- libudev: fix memleak when enumerating childs

* Wed Sep 04 2013 Harald Hoyer <harald@redhat.com> 206-10
- Do not require grubby, lorax now takes care of grubby
- cherry-picked a lot of patches from upstream

* Tue Aug 27 2013 Dennis Gilmore <dennis@ausil.us> - 206-9
- Require grubby, Fedora installs require grubby,
- kernel-install took over from new-kernel-pkg
- without the Requires we are unable to compose Fedora
- everyone else says that since kernel-install took over
- it is responsible for ensuring that grubby is in place
- this is really what we want for Fedora

* Tue Aug 27 2013 Kay Sievers <kay@redhat.com> - 206-8
- Revert "Require grubby its needed by kernel-install"

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> 206-7
- Require grubby its needed by kernel-install

* Thu Aug 22 2013 Harald Hoyer <harald@redhat.com> 206-6
- kernel-install now understands kernel flavors like PAE

* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 206-5
- add sddm.service to preset file (#998978)

* Fri Aug 16 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 206-4
- Filter out provides for private python modules.
- Add requires on kmod >= 14 (#990994).

* Sun Aug 11 2013 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 206-3
- New systemd-python3 package (#976427).
- Add ownership of a few directories that we create (#894202).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Kay Sievers <kay@redhat.com> - 206-1
- New upstream release
  Resolves (#984152)

* Wed Jul  3 2013 Lennart Poettering <lpoetter@redhat.com> - 205-1
- New upstream release

* Wed Jun 26 2013 Michal Schmidt <mschmidt@redhat.com> 204-10
- Split systemd-journal-gateway subpackage (#908081).

* Mon Jun 24 2013 Michal Schmidt <mschmidt@redhat.com> 204-9
- Rename nm_dispatcher to NetworkManager-dispatcher in default preset (#977433)

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 204-8
- fix, which helps to sucessfully browse journals with
  duplicated seqnums

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 204-7
- fix duplicate message ID bug
Resolves: rhbz#974132

* Thu Jun 06 2013 Harald Hoyer <harald@redhat.com> 204-6
- introduce 99-default-disable.preset

* Thu Jun  6 2013 Lennart Poettering <lpoetter@redhat.com> - 204-5
- Rename 90-display-manager.preset to 85-display-manager.preset so that it actually takes precedence over 90-default.preset's "disable *" line (#903690)

* Tue May 28 2013 Harald Hoyer <harald@redhat.com> 204-4
- Fix kernel-install (#965897)

* Wed May 22 2013 Kay Sievers <kay@redhat.com> - 204-3
- Fix kernel-install (#965897)

* Thu May  9 2013 Lennart Poettering <lpoetter@redhat.com> - 204-2
- New upstream release
- disable isdn by default (#959793)

* Tue May 07 2013 Harald Hoyer <harald@redhat.com> 203-2
- forward port kernel-install-grubby.patch

* Tue May  7 2013 Lennart Poettering <lpoetter@redhat.com> - 203-1
- New upstream release

* Wed Apr 24 2013 Harald Hoyer <harald@redhat.com> 202-3
- fix ENOENT for getaddrinfo
- Resolves: rhbz#954012 rhbz#956035
- crypt-setup-generator: correctly check return of strdup
- logind-dbus: initialize result variable
- prevent library underlinking

* Fri Apr 19 2013 Harald Hoyer <harald@redhat.com> 202-2
- nspawn create empty /etc/resolv.conf if necessary
- python wrapper: add sd_journal_add_conjunction()
- fix s390 booting
- Resolves: rhbz#953217

* Thu Apr 18 2013 Lennart Poettering <lpoetter@redhat.com> - 202-1
- New upstream release

* Tue Apr 09 2013 Michal Schmidt <mschmidt@redhat.com> - 201-2
- Automatically discover whether to run autoreconf and add autotools and git
  BuildRequires based on the presence of patches to be applied.
- Use find -delete.

* Mon Apr  8 2013 Lennart Poettering <lpoetter@redhat.com> - 201-1
- New upstream release

* Mon Apr  8 2013 Lennart Poettering <lpoetter@redhat.com> - 200-4
- Update preset file

* Fri Mar 29 2013 Lennart Poettering <lpoetter@redhat.com> - 200-3
- Remove NetworkManager-wait-online.service from presets file again, it should default to off

* Fri Mar 29 2013 Lennart Poettering <lpoetter@redhat.com> - 200-2
- New upstream release

* Tue Mar 26 2013 Lennart Poettering <lpoetter@redhat.com> - 199-2
- Add NetworkManager-wait-online.service to the presets file

* Tue Mar 26 2013 Lennart Poettering <lpoetter@redhat.com> - 199-1
- New upstream release

* Mon Mar 18 2013 Michal Schmidt <mschmidt@redhat.com> 198-7
- Drop /usr/s?bin/ prefixes.

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 198-6
- run autogen to pickup all changes

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 198-5
- do not mount anything, when not running as pid 1
- add initrd.target for systemd in the initrd

* Wed Mar 13 2013 Harald Hoyer <harald@redhat.com> 198-4
- fix switch-root and local-fs.target problem
- patch kernel-install to use grubby, if available

* Fri Mar 08 2013 Harald Hoyer <harald@redhat.com> 198-3
- add Conflict with dracut < 026 because of the new switch-root isolate

* Thu Mar  7 2013 Lennart Poettering <lpoetter@redhat.com> - 198-2
- Create required users

* Thu Mar 7 2013 Lennart Poettering <lpoetter@redhat.com> - 198-1
- New release
- Enable journal persistancy by default

* Sun Feb 10 2013 Peter Robinson <pbrobinson@fedoraproject.org> 197-3
- Bump for ARM

* Fri Jan 18 2013 Michal Schmidt <mschmidt@redhat.com> - 197-2
- Added qemu-guest-agent.service to presets (Lennart, #885406).
- Add missing pygobject3-base to systemd-analyze deps (Lennart).
- Do not require hwdata, it is all in the hwdb now (Kay).
- Drop dependency on dbus-python.

* Tue Jan  8 2013 Lennart Poettering <lpoetter@redhat.com> - 197-1
- New upstream release

* Mon Dec 10 2012 Michal Schmidt <mschmidt@redhat.com> - 196-4
- Enable rngd.service by default (#857765).

* Mon Dec 10 2012 Michal Schmidt <mschmidt@redhat.com> - 196-3
- Disable hardening on s390(x) because PIE is broken there and produces
  text relocations with __thread (#868839).

* Wed Dec 05 2012 Michal Schmidt <mschmidt@redhat.com> - 196-2
- added spice-vdagentd.service to presets (Lennart, #876237)
- BR cryptsetup-devel instead of the legacy cryptsetup-luks-devel provide name
  (requested by Milan Brož).
- verbose make to see the actual build flags

* Wed Nov 21 2012 Lennart Poettering <lpoetter@redhat.com> - 196-1
- New upstream release

* Tue Nov 20 2012 Lennart Poettering <lpoetter@redhat.com> - 195-8
- https://bugzilla.redhat.com/show_bug.cgi?id=873459
- https://bugzilla.redhat.com/show_bug.cgi?id=878093

* Thu Nov 15 2012 Michal Schmidt <mschmidt@redhat.com> - 195-7
- Revert udev killing cgroup patch for F18 Beta.
- https://bugzilla.redhat.com/show_bug.cgi?id=873576

* Fri Nov 09 2012 Michal Schmidt <mschmidt@redhat.com> - 195-6
- Fix cyclical dep between systemd and systemd-libs.
- Avoid broken build of test-journal-syslog.
- https://bugzilla.redhat.com/show_bug.cgi?id=873387
- https://bugzilla.redhat.com/show_bug.cgi?id=872638

* Thu Oct 25 2012 Kay Sievers <kay@redhat.com> - 195-5
- require 'sed', limit HOSTNAME= match

* Wed Oct 24 2012 Michal Schmidt <mschmidt@redhat.com> - 195-4
- add dmraid-activation.service to the default preset
- add yum protected.d fragment
- https://bugzilla.redhat.com/show_bug.cgi?id=869619
- https://bugzilla.redhat.com/show_bug.cgi?id=869717

* Wed Oct 24 2012 Kay Sievers <kay@redhat.com> - 195-3
- Migrate /etc/sysconfig/ i18n, keyboard, network files/variables to
  systemd native files

* Tue Oct 23 2012 Lennart Poettering <lpoetter@redhat.com> - 195-2
- Provide syslog because the journal is fine as a syslog implementation

* Tue Oct 23 2012 Lennart Poettering <lpoetter@redhat.com> - 195-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=831665
- https://bugzilla.redhat.com/show_bug.cgi?id=847720
- https://bugzilla.redhat.com/show_bug.cgi?id=858693
- https://bugzilla.redhat.com/show_bug.cgi?id=863481
- https://bugzilla.redhat.com/show_bug.cgi?id=864629
- https://bugzilla.redhat.com/show_bug.cgi?id=864672
- https://bugzilla.redhat.com/show_bug.cgi?id=864674
- https://bugzilla.redhat.com/show_bug.cgi?id=865128
- https://bugzilla.redhat.com/show_bug.cgi?id=866346
- https://bugzilla.redhat.com/show_bug.cgi?id=867407
- https://bugzilla.redhat.com/show_bug.cgi?id=868603

* Wed Oct 10 2012 Michal Schmidt <mschmidt@redhat.com> - 194-2
- Add scriptlets for migration away from systemd-timedated-ntp.target

* Wed Oct  3 2012 Lennart Poettering <lpoetter@redhat.com> - 194-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=859614
- https://bugzilla.redhat.com/show_bug.cgi?id=859655

* Fri Sep 28 2012 Lennart Poettering <lpoetter@redhat.com> - 193-1
- New upstream release

* Tue Sep 25 2012 Lennart Poettering <lpoetter@redhat.com> - 192-1
- New upstream release

* Fri Sep 21 2012 Lennart Poettering <lpoetter@redhat.com> - 191-2
- Fix journal mmap header prototype definition to fix compilation on 32bit

* Fri Sep 21 2012 Lennart Poettering <lpoetter@redhat.com> - 191-1
- New upstream release
- Enable all display managers by default, as discussed with Adam Williamson

* Thu Sep 20 2012 Lennart Poettering <lpoetter@redhat.com> - 190-1
- New upstream release
- Take possession of /etc/localtime, and remove /etc/sysconfig/clock
- https://bugzilla.redhat.com/show_bug.cgi?id=858780
- https://bugzilla.redhat.com/show_bug.cgi?id=858787
- https://bugzilla.redhat.com/show_bug.cgi?id=858771
- https://bugzilla.redhat.com/show_bug.cgi?id=858754
- https://bugzilla.redhat.com/show_bug.cgi?id=858746
- https://bugzilla.redhat.com/show_bug.cgi?id=858266
- https://bugzilla.redhat.com/show_bug.cgi?id=858224
- https://bugzilla.redhat.com/show_bug.cgi?id=857670
- https://bugzilla.redhat.com/show_bug.cgi?id=856975
- https://bugzilla.redhat.com/show_bug.cgi?id=855863
- https://bugzilla.redhat.com/show_bug.cgi?id=851970
- https://bugzilla.redhat.com/show_bug.cgi?id=851275
- https://bugzilla.redhat.com/show_bug.cgi?id=851131
- https://bugzilla.redhat.com/show_bug.cgi?id=847472
- https://bugzilla.redhat.com/show_bug.cgi?id=847207
- https://bugzilla.redhat.com/show_bug.cgi?id=846483
- https://bugzilla.redhat.com/show_bug.cgi?id=846085
- https://bugzilla.redhat.com/show_bug.cgi?id=845973
- https://bugzilla.redhat.com/show_bug.cgi?id=845194
- https://bugzilla.redhat.com/show_bug.cgi?id=845028
- https://bugzilla.redhat.com/show_bug.cgi?id=844630
- https://bugzilla.redhat.com/show_bug.cgi?id=839736
- https://bugzilla.redhat.com/show_bug.cgi?id=835848
- https://bugzilla.redhat.com/show_bug.cgi?id=831740
- https://bugzilla.redhat.com/show_bug.cgi?id=823485
- https://bugzilla.redhat.com/show_bug.cgi?id=821813
- https://bugzilla.redhat.com/show_bug.cgi?id=807886
- https://bugzilla.redhat.com/show_bug.cgi?id=802198
- https://bugzilla.redhat.com/show_bug.cgi?id=767795
- https://bugzilla.redhat.com/show_bug.cgi?id=767561
- https://bugzilla.redhat.com/show_bug.cgi?id=752774
- https://bugzilla.redhat.com/show_bug.cgi?id=732874
- https://bugzilla.redhat.com/show_bug.cgi?id=858735

* Thu Sep 13 2012 Lennart Poettering <lpoetter@redhat.com> - 189-4
- Don't pull in pkg-config as dep
- https://bugzilla.redhat.com/show_bug.cgi?id=852828

* Wed Sep 12 2012 Lennart Poettering <lpoetter@redhat.com> - 189-3
- Update preset policy
- Rename preset policy file from 99-default.preset to 90-default.preset so that people can order their own stuff after the Fedora default policy if they wish

* Thu Aug 23 2012 Lennart Poettering <lpoetter@redhat.com> - 189-2
- Update preset policy
- https://bugzilla.redhat.com/show_bug.cgi?id=850814

* Thu Aug 23 2012 Lennart Poettering <lpoetter@redhat.com> - 189-1
- New upstream release

* Thu Aug 16 2012 Ray Strode <rstrode@redhat.com> 188-4
- more scriptlet fixes
  (move dm migration logic to %%posttrans so the service
   files it's looking for are available at the time
   the logic is run)

* Sat Aug 11 2012 Lennart Poettering <lpoetter@redhat.com> - 188-3
- Remount file systems MS_PRIVATE before switching roots
- https://bugzilla.redhat.com/show_bug.cgi?id=847418

* Wed Aug 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 188-2
- fix scriptlets

* Wed Aug  8 2012 Lennart Poettering <lpoetter@redhat.com> - 188-1
- New upstream release
- Enable gdm and avahi by default via the preset file
- Convert /etc/sysconfig/desktop to display-manager.service symlink
- Enable hardened build

* Mon Jul 30 2012 Kay Sievers <kay@redhat.com> - 187-3
- Obsolete: system-setup-keyboard

* Wed Jul 25 2012 Kalev Lember <kalevlember@gmail.com> - 187-2
- Run ldconfig for the new -libs subpackage

* Thu Jul 19 2012 Lennart Poettering <lpoetter@redhat.com> - 187-1
- New upstream release

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 186-2
- fixed dracut conflict version

* Tue Jul  3 2012 Lennart Poettering <lpoetter@redhat.com> - 186-1
- New upstream release

* Fri Jun 22 2012 Nils Philippsen <nils@redhat.com> - 185-7.gite7aee75
- add obsoletes/conflicts so multilib systemd -> systemd-libs updates work

* Thu Jun 14 2012 Michal Schmidt <mschmidt@redhat.com> - 185-6.gite7aee75
- Update to current git

* Wed Jun 06 2012 Kay Sievers - 185-5.gita2368a3
- disable plymouth in configure, to drop the .wants/ symlinks

* Wed Jun 06 2012 Michal Schmidt <mschmidt@redhat.com> - 185-4.gita2368a3
- Update to current git snapshot
  - Add systemd-readahead-analyze
  - Drop upstream patch
- Split systemd-libs
- Drop duplicate doc files
- Fixed License headers of subpackages

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 185-3
- Drop plymouth files
- Conflict with old plymouth

* Tue Jun 05 2012 Kay Sievers - 185-2
- selinux udev labeling fix
- conflict with older dracut versions for new udev file names

* Mon Jun 04 2012 Kay Sievers - 185-1
- New upstream release
  - udev selinux labeling fixes
  - new man pages
  - systemctl help <unit name>

* Thu May 31 2012 Lennart Poettering <lpoetter@redhat.com> - 184-1
- New upstream release

* Thu May 24 2012 Kay Sievers <kay@redhat.com> - 183-1
- New upstream release including udev merge.

* Wed Mar 28 2012 Michal Schmidt <mschmidt@redhat.com> - 44-4
- Add triggers from Bill Nottingham to correct the damage done by
  the obsoleted systemd-units's preun scriptlet (#807457).

* Mon Mar 26 2012 Dennis Gilmore <dennis@ausil.us> - 44-3
- apply patch from upstream so we can build systemd on arm and ppc
- and likely the rest of the secondary arches

* Tue Mar 20 2012 Michal Schmidt <mschmidt@redhat.com> - 44-2
- Don't build the gtk parts anymore. They're moving into systemd-ui.
- Remove a dead patch file.

* Fri Mar 16 2012 Lennart Poettering <lpoetter@redhat.com> - 44-1
- New upstream release
- Closes #798760, #784921, #783134, #768523, #781735

* Mon Feb 27 2012 Dennis Gilmore <dennis@ausil.us> - 43-2
- don't conflict with fedora-release systemd never actually provided
- /etc/os-release so there is no actual conflict

* Wed Feb 15 2012 Lennart Poettering <lpoetter@redhat.com> - 43-1
- New upstream release
- Closes #789758, #790260, #790522

* Sat Feb 11 2012 Lennart Poettering <lpoetter@redhat.com> - 42-1
- New upstream release
- Save a bit of entropy during system installation (#789407)
- Don't own /etc/os-release anymore, leave that to fedora-release

* Thu Feb  9 2012 Adam Williamson <awilliam@redhat.com> - 41-2
- rebuild for fixed binutils

* Thu Feb  9 2012 Lennart Poettering <lpoetter@redhat.com> - 41-1
- New upstream release

* Tue Feb  7 2012 Lennart Poettering <lpoetter@redhat.com> - 40-1
- New upstream release

* Thu Jan 26 2012 Kay Sievers <kay@redhat.com> - 39-3
- provide /sbin/shutdown

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 39-2
- increment release

* Wed Jan 25 2012 Kay Sievers <kay@redhat.com> - 39-1.1
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Wed Jan 25 2012 Lennart Poettering <lpoetter@redhat.com> - 39-1
- New upstream release

* Sun Jan 22 2012 Michal Schmidt <mschmidt@redhat.com> - 38-6.git9fa2f41
- Update to a current git snapshot.
- Resolves: #781657

* Sun Jan 22 2012 Michal Schmidt <mschmidt@redhat.com> - 38-5
- Build against libgee06. Reenable gtk tools.
- Delete unused patches.
- Add easy building of git snapshots.
- Remove legacy spec file elements.
- Don't mention implicit BuildRequires.
- Configure with --disable-static.
- Merge -units into the main package.
- Move section 3 manpages to -devel.
- Fix unowned directory.
- Run ldconfig in scriptlets.
- Split systemd-analyze to a subpackage.

* Sat Jan 21 2012 Dan Horák <dan[at]danny.cz> - 38-4
- fix build on big-endians

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-3
- Disable building of gtk tools for now

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-2
- Fix a few (build) dependencies

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-1
- New upstream release

* Tue Nov 15 2011 Michal Schmidt <mschmidt@redhat.com> - 37-4
- Run authconfig if /etc/pam.d/system-auth is not a symlink.
- Resolves: #753160

* Wed Nov 02 2011 Michal Schmidt <mschmidt@redhat.com> - 37-3
- Fix remote-fs-pre.target and its ordering.
- Resolves: #749940

* Wed Oct 19 2011 Michal Schmidt <mschmidt@redhat.com> - 37-2
- A couple of fixes from upstream:
- Fix a regression in bash-completion reported in Bodhi.
- Fix a crash in isolating.
- Resolves: #717325

* Tue Oct 11 2011 Lennart Poettering <lpoetter@redhat.com> - 37-1
- New upstream release
- Resolves: #744726, #718464, #713567, #713707, #736756

* Thu Sep 29 2011 Michal Schmidt <mschmidt@redhat.com> - 36-5
- Undo the workaround. Kay says it does not belong in systemd.
- Unresolves: #741655

* Thu Sep 29 2011 Michal Schmidt <mschmidt@redhat.com> - 36-4
- Workaround for the crypto-on-lvm-on-crypto disk layout
- Resolves: #741655

* Sun Sep 25 2011 Michal Schmidt <mschmidt@redhat.com> - 36-3
- Revert an upstream patch that caused ordering cycles
- Resolves: #741078

* Fri Sep 23 2011 Lennart Poettering <lpoetter@redhat.com> - 36-2
- Add /etc/timezone to ghosted files

* Fri Sep 23 2011 Lennart Poettering <lpoetter@redhat.com> - 36-1
- New upstream release
- Resolves: #735013, #736360, #737047, #737509, #710487, #713384

* Thu Sep  1 2011 Lennart Poettering <lpoetter@redhat.com> - 35-1
- New upstream release
- Update post scripts
- Resolves: #726683, #713384, #698198, #722803, #727315, #729997, #733706, #734611

* Thu Aug 25 2011 Lennart Poettering <lpoetter@redhat.com> - 34-1
- New upstream release

* Fri Aug 19 2011 Harald Hoyer <harald@redhat.com> 33-2
- fix ABRT on service file reloading
- Resolves: rhbz#732020

* Wed Aug  3 2011 Lennart Poettering <lpoetter@redhat.com> - 33-1
- New upstream release

* Fri Jul 29 2011 Lennart Poettering <lpoetter@redhat.com> - 32-1
- New upstream release

* Wed Jul 27 2011 Lennart Poettering <lpoetter@redhat.com> - 31-2
- Fix access mode of modprobe file, restart logind after upgrade

* Wed Jul 27 2011 Lennart Poettering <lpoetter@redhat.com> - 31-1
- New upstream release

* Wed Jul 13 2011 Lennart Poettering <lpoetter@redhat.com> - 30-1
- New upstream release

* Thu Jun 16 2011 Lennart Poettering <lpoetter@redhat.com> - 29-1
- New upstream release

* Mon Jun 13 2011 Michal Schmidt <mschmidt@redhat.com> - 28-4
- Apply patches from current upstream.
- Fixes memory size detection on 32-bit with >4GB RAM (BZ712341)

* Wed Jun 08 2011 Michal Schmidt <mschmidt@redhat.com> - 28-3
- Apply patches from current upstream
- https://bugzilla.redhat.com/show_bug.cgi?id=709909
- https://bugzilla.redhat.com/show_bug.cgi?id=710839
- https://bugzilla.redhat.com/show_bug.cgi?id=711015

* Sat May 28 2011 Lennart Poettering <lpoetter@redhat.com> - 28-2
- Pull in nss-myhostname

* Thu May 26 2011 Lennart Poettering <lpoetter@redhat.com> - 28-1
- New upstream release

* Wed May 25 2011 Lennart Poettering <lpoetter@redhat.com> - 26-2
- Bugfix release
- https://bugzilla.redhat.com/show_bug.cgi?id=707507
- https://bugzilla.redhat.com/show_bug.cgi?id=707483
- https://bugzilla.redhat.com/show_bug.cgi?id=705427
- https://bugzilla.redhat.com/show_bug.cgi?id=707577

* Sat Apr 30 2011 Lennart Poettering <lpoetter@redhat.com> - 26-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=699394
- https://bugzilla.redhat.com/show_bug.cgi?id=698198
- https://bugzilla.redhat.com/show_bug.cgi?id=698674
- https://bugzilla.redhat.com/show_bug.cgi?id=699114
- https://bugzilla.redhat.com/show_bug.cgi?id=699128

* Thu Apr 21 2011 Lennart Poettering <lpoetter@redhat.com> - 25-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=694788
- https://bugzilla.redhat.com/show_bug.cgi?id=694321
- https://bugzilla.redhat.com/show_bug.cgi?id=690253
- https://bugzilla.redhat.com/show_bug.cgi?id=688661
- https://bugzilla.redhat.com/show_bug.cgi?id=682662
- https://bugzilla.redhat.com/show_bug.cgi?id=678555
- https://bugzilla.redhat.com/show_bug.cgi?id=628004

* Wed Apr  6 2011 Lennart Poettering <lpoetter@redhat.com> - 24-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=694079
- https://bugzilla.redhat.com/show_bug.cgi?id=693289
- https://bugzilla.redhat.com/show_bug.cgi?id=693274
- https://bugzilla.redhat.com/show_bug.cgi?id=693161

* Tue Apr  5 2011 Lennart Poettering <lpoetter@redhat.com> - 23-1
- New upstream release
- Include systemd-sysv-convert

* Fri Apr  1 2011 Lennart Poettering <lpoetter@redhat.com> - 22-1
- New upstream release

* Wed Mar 30 2011 Lennart Poettering <lpoetter@redhat.com> - 21-2
- The quota services are now pulled in by mount points, hence no need to enable them explicitly

* Tue Mar 29 2011 Lennart Poettering <lpoetter@redhat.com> - 21-1
- New upstream release

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> - 20-2
- Apply upstream patch to not send untranslated messages to plymouth

* Tue Mar  8 2011 Lennart Poettering <lpoetter@redhat.com> - 20-1
- New upstream release

* Tue Mar  1 2011 Lennart Poettering <lpoetter@redhat.com> - 19-1
- New upstream release

* Wed Feb 16 2011 Lennart Poettering <lpoetter@redhat.com> - 18-1
- New upstream release

* Mon Feb 14 2011 Bill Nottingham <notting@redhat.com> - 17-6
- bump upstart obsoletes (#676815)

* Wed Feb  9 2011 Tom Callaway <spot@fedoraproject.org> - 17-5
- add macros.systemd file for %%{_unitdir}

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  9 2011 Lennart Poettering <lpoetter@redhat.com> - 17-3
- Fix popen() of systemctl, #674916

* Mon Feb  7 2011 Bill Nottingham <notting@redhat.com> - 17-2
- add epoch to readahead obsolete

* Sat Jan 22 2011 Lennart Poettering <lpoetter@redhat.com> - 17-1
- New upstream release

* Tue Jan 18 2011 Lennart Poettering <lpoetter@redhat.com> - 16-2
- Drop console.conf again, since it is not shipped in pamtmp.conf

* Sat Jan  8 2011 Lennart Poettering <lpoetter@redhat.com> - 16-1
- New upstream release

* Thu Nov 25 2010 Lennart Poettering <lpoetter@redhat.com> - 15-1
- New upstream release

* Thu Nov 25 2010 Lennart Poettering <lpoetter@redhat.com> - 14-1
- Upstream update
- Enable hwclock-load by default
- Obsolete readahead
- Enable /var/run and /var/lock on tmpfs

* Fri Nov 19 2010 Lennart Poettering <lpoetter@redhat.com> - 13-1
- new upstream release

* Wed Nov 17 2010 Bill Nottingham <notting@redhat.com> 12-3
- Fix clash

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 12-2
- Don't clash with initscripts for now, so that we don't break the builders

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 12-1
- New upstream release

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> - 11-2
- Rebuild with newer vala, libnotify

* Thu Oct  7 2010 Lennart Poettering <lpoetter@redhat.com> - 11-1
- New upstream release

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 10-6
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Bill Nottingham <notting@redhat.com> - 10-5
- merge -sysvinit into main package

* Mon Sep 20 2010 Bill Nottingham <notting@redhat.com> - 10-4
- obsolete upstart-sysvinit too

* Fri Sep 17 2010 Bill Nottingham <notting@redhat.com> - 10-3
- Drop upstart requires

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 10-2
- Enable audit
- https://bugzilla.redhat.com/show_bug.cgi?id=633771

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 10-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=630401
- https://bugzilla.redhat.com/show_bug.cgi?id=630225
- https://bugzilla.redhat.com/show_bug.cgi?id=626966
- https://bugzilla.redhat.com/show_bug.cgi?id=623456

* Fri Sep  3 2010 Bill Nottingham <notting@redhat.com> - 9-3
- move fedora-specific units to initscripts; require newer version thereof

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 9-2
- Add missing tarball

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 9-1
- New upstream version
- Closes 501720, 614619, 621290, 626443, 626477, 627014, 627785, 628913

* Fri Aug 27 2010 Lennart Poettering <lpoetter@redhat.com> - 8-3
- Reexecute after installation, take ownership of /var/run/user
- https://bugzilla.redhat.com/show_bug.cgi?id=627457
- https://bugzilla.redhat.com/show_bug.cgi?id=627634

* Thu Aug 26 2010 Lennart Poettering <lpoetter@redhat.com> - 8-2
- Properly create default.target link

* Wed Aug 25 2010 Lennart Poettering <lpoetter@redhat.com> - 8-1
- New upstream release

* Thu Aug 12 2010 Lennart Poettering <lpoetter@redhat.com> - 7-3
- Fix https://bugzilla.redhat.com/show_bug.cgi?id=623561

* Thu Aug 12 2010 Lennart Poettering <lpoetter@redhat.com> - 7-2
- Fix https://bugzilla.redhat.com/show_bug.cgi?id=623430

* Tue Aug 10 2010 Lennart Poettering <lpoetter@redhat.com> - 7-1
- New upstream release

* Fri Aug  6 2010 Lennart Poettering <lpoetter@redhat.com> - 6-2
- properly hide output on package installation
- pull in coreutils during package installtion

* Fri Aug  6 2010 Lennart Poettering <lpoetter@redhat.com> - 6-1
- New upstream release
- Fixes #621200

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 5-2
- Add tarball

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 5-1
- Prepare release 5

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 4-4
- Add 'sysvinit-userspace' provide to -sysvinit package to fix upgrade/install (#618537)

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-3
- Add libselinux to build dependencies

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-2
- Use the right tarball

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-1
- New upstream release, and make default

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-3
- Used wrong tarball

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-2
- Own /cgroup jointly with libcgroup, since we don't dpend on it anymore

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-1
- New upstream release

* Fri Jul 9 2010 Lennart Poettering <lpoetter@redhat.com> - 2-0
- New upstream release

* Wed Jul 7 2010 Lennart Poettering <lpoetter@redhat.com> - 1-0
- First upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.7.20100629git4176e5
- New snapshot
- Split off -units package where other packages can depend on without pulling in the whole of systemd

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.6.20100622gita3723b
- Add missing libtool dependency.

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.5.20100622gita3723b
- Update snapshot

* Mon Jun 14 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.4.20100614git393024
- Pull the latest snapshot that fixes a segfault. Resolves rhbz#603231

* Fri Jun 11 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.3.20100610git2f198e
- More minor fixes as per review

* Thu Jun 10 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.2.20100610git2f198e
- Spec improvements from David Hollis

* Wed Jun 09 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.1.20090609git2f198e
- Address review comments

* Tue Jun 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.0.git2010-06-02
- Initial spec (adopted from Kay Sievers)
