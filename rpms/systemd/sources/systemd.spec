#global commit f02b5472c6f0c41e5dc8dc2c84590866baf937ff
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

#global stable 1

# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

%global pkgdir %{_prefix}/lib/systemd
%global system_unit_dir %{pkgdir}/system
%global user_unit_dir %{pkgdir}/user

Name:           systemd
Url:            https://www.freedesktop.org/wiki/Software/systemd
Version:        241
Release:        1%{?commit:.git%{shortcommit}}%{?dist}
# For a breakdown of the licensing, see README
License:        LGPLv2+ and MIT and GPLv2+
Summary:        System and Service Manager

%global github_version %(c=%{version}; echo ${c}|tr '~' '-')

# download tarballs with "spectool -g systemd.spec"
%if %{defined commit}
Source0:        https://github.com/systemd/systemd%{?stable:-stable}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/systemd/systemd/archive/v%{github_version}/%{name}-%{github_version}.tar.gz
%endif
# This file must be available before %%prep.
# It is generated during systemd build and can be found in build/src/core/.
Source1:        triggers.systemd
Source2:        split-files.py
Source3:        purge-nobody-user

# Prevent accidental removal of the systemd package
Source4:        yum-protect-systemd.conf

Source5:        inittab
Source6:        sysctl.conf.README
Source7:        systemd-journal-remote.xml
Source8:        systemd-journal-gatewayd.xml
Source9:        20-yama-ptrace.conf
Source10:       systemd-udev-trigger-no-reload.conf
Source11:       20-grubby.install
Source12:       systemd-user

%if 0
GIT_DIR=../../src/systemd/.git git format-patch-ab --no-signature -M -N v235..v235-stable
i=1; for j in 00*patch; do printf "Patch%04d:      %s\n" $i $j; i=$((i+1));done|xclip
GIT_DIR=../../src/systemd/.git git diffab -M v233..master@{2017-06-15} -- hwdb/[67]* hwdb/parse_hwdb.py > hwdb.patch
%endif

Patch0002:      0002-Revert-units-set-NoNewPrivileges-for-all-long-runnin.patch

Patch0998:      0998-resolved-create-etc-resolv.conf-symlink-at-runtime.patch

%ifarch %{ix86} x86_64 aarch64
%global have_gnu_efi 1
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
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
BuildRequires:  xz
BuildRequires:  lz4-devel
BuildRequires:  lz4
BuildRequires:  bzip2-devel
BuildRequires:  libidn2-devel
BuildRequires:  libcurl-devel
BuildRequires:  kmod-devel
BuildRequires:  elfutils-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  gnutls-devel
BuildRequires:  qrencode-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  iptables-devel
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  pkgconfig
BuildRequires:  gperf
BuildRequires:  gawk
BuildRequires:  tree
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
BuildRequires:  firewalld-filesystem
%if 0%{?have_gnu_efi}
BuildRequires:  gnu-efi gnu-efi-devel
%endif
BuildRequires:  libseccomp-devel
BuildRequires:  git
BuildRequires:  meson >= 0.43
BuildRequires:  gettext
# We use RUNNING_ON_VALGRIND in tests, so the headers need to be available
BuildRequires:  valgrind-devel

Requires(post): coreutils
Requires(post): sed
Requires(post): acl
Requires(post): grep
# systemd-machine-id-setup requires libssl
Requires(post): openssl-libs
Requires(pre):  coreutils
Requires(pre):  /usr/bin/getent
Requires(pre):  /usr/sbin/groupadd
Requires:       dbus >= 1.9.18
Requires:       %{name}-pam = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
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
Provides:       systemd-sysv = 206
Conflicts:      initscripts < 9.56.1
%if 0%{?fedora}
Conflicts:      fedora-release < 23-0.12
%endif

%description
systemd is a system and service manager that runs as PID 1 and starts
the rest of the system. It provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux control groups, maintains mount and automount points, and
implements an elaborate transactional dependency-based service control
logic. systemd supports SysV and LSB init scripts and works as a
replacement for sysvinit. Other parts of this package are a logging daemon,
utilities to control basic system configuration like the hostname,
date, locale, maintain a list of logged-in users, system accounts,
runtime directories and settings, and daemons to manage simple network
configuration, network time synchronization, log forwarding, and name
resolution.

%package libs
Summary:        systemd libraries
License:        LGPLv2+ and MIT
Obsoletes:      libudev < 183
Obsoletes:      systemd < 185-4
Conflicts:      systemd < 185-4
Obsoletes:      systemd-compat-libs < 230
Obsoletes:      nss-myhostname < 0.4
Provides:       nss-myhostname = 0.4
Provides:       nss-myhostname%{_isa} = 0.4
Requires(post): coreutils
Requires(post): sed
Requires(post): grep
Requires(post): /usr/bin/getent

%description libs
Libraries for systemd and udev.

%package pam
Summary:        systemd PAM module
Requires:       %{name} = %{version}-%{release}

%description pam
Systemd PAM module registers the session with systemd-logind.

%package rpm-macros
Summary:        Macros that define paths and scriptlets related to systemd
BuildArch:      noarch

%description rpm-macros
Just the definitions of rpm macros. Use %%{?systemd_requires} in the
binary packages that use any scriptlets from this package.

%package devel
Summary:        Development headers for systemd
License:        LGPLv2+ and MIT
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       libudev-devel = %{version}
Provides:       libudev-devel%{_isa} = %{version}
Obsoletes:      libudev-devel < 183
# Fake dependency to make sure systemd-pam is pulled into multilib (#1414153)
Requires:       %{name}-pam = %{version}-%{release}

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
Provides:       udev%{_isa} = %{version}
Obsoletes:      udev < 183
# https://bugzilla.redhat.com/show_bug.cgi?id=1377733#c9
Recommends:     systemd-bootchart
# https://bugzilla.redhat.com/show_bug.cgi?id=1408878
Recommends:     kbd
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
Requires:       firewalld-filesystem
Provides:       %{name}-journal-gateway = %{version}-%{release}
Provides:       %{name}-journal-gateway%{_isa} = %{version}-%{release}
Obsoletes:      %{name}-journal-gateway < 227-7

%description journal-remote
Programs to forward journal entries over the network, using encrypted HTTP,
and to write journal files from serialized journal contents.

This package contains systemd-journal-gatewayd,
systemd-journal-remote, and systemd-journal-upload.

%package tests
Summary:       Internal unit tests for systemd
Requires:      %{name}%{?_isa} = %{version}-%{release}
License:       LGPLv2+

%description tests
"Installed tests" that are usually run as part of the build system.
They can be useful to test systemd internals.

%prep
%autosetup -n %{?commit:%{name}%{?stable:-stable}-%{commit}}%{!?commit:%{name}%{?stable:-stable}-%{github_version}} -p1 -Sgit

%build
%define ntpvendor %(source /etc/os-release; echo ${ID})
%{!?ntpvendor: echo 'NTP vendor zone is not set!'; exit 1}

CONFIGURE_OPTS=(
        -Dsysvinit-path=/etc/rc.d/init.d
        -Drc-local=/etc/rc.d/rc.local
        -Dntp-servers='0.%{ntpvendor}.pool.ntp.org 1.%{ntpvendor}.pool.ntp.org 2.%{ntpvendor}.pool.ntp.org 3.%{ntpvendor}.pool.ntp.org'
        -Ddev-kvm-mode=0666
        -Dkmod=true
        -Dxkbcommon=true
        -Dblkid=true
        -Dseccomp=true
        -Dima=true
        -Dselinux=true
        -Dapparmor=false
        -Dpolkit=true
        -Dxz=true
        -Dzlib=true
        -Dbzip2=true
        -Dlz4=true
        -Dpam=true
        -Dacl=true
        -Dsmack=true
        -Dgcrypt=true
        -Daudit=true
        -Delfutils=true
        -Dlibcryptsetup=true
        -Delfutils=true
        -Dqrencode=true
        -Dgnutls=true
        -Dmicrohttpd=true
        -Dlibidn2=true
        -Dlibiptc=true
        -Dlibcurl=true
        -Defi=true
        -Dgnu-efi=%{?have_gnu_efi:true}%{?!have_gnu_efi:false}
        -Dtpm=true
        -Dhwdb=true
        -Dsysusers=true
        -Ddefault-kill-user-processes=false
        -Dtests=unsafe
        -Dinstall-tests=true
        -Dtty-gid=5
        -Dusers-gid=100
        -Dnobody-user=nobody
        -Dnobody-group=nobody
        -Dsplit-usr=false
        -Dsplit-bin=true
        -Db_lto=true
        -Dversion-tag=v%{version}-%{release}
)

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

# udev links
mkdir -p %{buildroot}/%{_sbindir}
ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# Compatiblity and documentation files
touch %{buildroot}/etc/crypttab
chmod 600 %{buildroot}/etc/crypttab

# /etc/initab
install -Dm0644 -t %{buildroot}/etc/ %{SOURCE5}

# /etc/sysctl.conf compat
install -Dm0644 %{SOURCE6} %{buildroot}/etc/sysctl.conf
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
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/linger
mkdir -p %{buildroot}%{_localstatedir}/lib/private
mkdir -p %{buildroot}%{_localstatedir}/log/private
mkdir -p %{buildroot}%{_localstatedir}/cache/private
mkdir -p %{buildroot}%{_localstatedir}/lib/private/systemd/journal-upload
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/timesync
ln -s ../private/systemd/journal-upload %{buildroot}%{_localstatedir}/lib/systemd/journal-upload
mkdir -p %{buildroot}%{_localstatedir}/log/journal
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed
touch %{buildroot}%{_localstatedir}/lib/systemd/timesync/clock
touch %{buildroot}%{_localstatedir}/lib/private/systemd/journal-upload/state

# Install yum protection fragment
install -Dm0644 %{SOURCE4} %{buildroot}/etc/dnf/protected.d/systemd.conf

install -Dm0644 -t %{buildroot}/usr/lib/firewalld/services/ %{SOURCE7} %{SOURCE8}

# Restore systemd-user pam config from before "removal of Fedora-specific bits"
install -Dm0644 -t %{buildroot}/etc/pam.d/ %{SOURCE12}

# Install additional docs
# https://bugzilla.redhat.com/show_bug.cgi?id=1234951
install -Dm0644 -t %{buildroot}%{_pkgdocdir}/ %{SOURCE9}

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{system_unit_dir}/systemd-udev-trigger.service.d/ %{SOURCE10}

# A temporary work-around for https://bugzilla.redhat.com/show_bug.cgi?id=1663040
mkdir -p %{buildroot}%{system_unit_dir}/systemd-hostnamed.service.d/
cat >%{buildroot}%{system_unit_dir}/systemd-hostnamed.service.d/disable-privatedevices.conf <<EOF
[Service]
PrivateDevices=no
EOF

install -Dm0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE11}

install -D -t %{buildroot}/usr/lib/systemd/ %{SOURCE3}

sed -i 's|#!/usr/bin/env python3|#!%{__python3}|' %{buildroot}/usr/lib/systemd/tests/run-unit-tests.py

%find_lang %{name}

# Split files in build root into rpms. See split-files.py for the
# rules towards the end, anything which is an exception needs a line
# here.
python3 %{SOURCE2} %buildroot <<EOF
%ghost %config(noreplace) /etc/crypttab
%ghost /etc/udev/hwdb.bin
/etc/inittab
/usr/lib/systemd/purge-nobody-user
%ghost %config(noreplace) /etc/vconsole.conf
%ghost %config(noreplace) /etc/X11/xorg.conf.d/00-keyboard.conf
%ghost %attr(0664,root,utmp) /var/run/utmp
%ghost %attr(0664,root,utmp) /var/log/wtmp
%ghost %attr(0600,root,utmp) /var/log/btmp
%ghost %config(noreplace) /etc/hostname
%ghost %config(noreplace) /etc/localtime
%ghost %config(noreplace) /etc/locale.conf
%ghost %config(noreplace) /etc/machine-id
%ghost %config(noreplace) /etc/machine-info
%ghost %attr(0700,root,root) %dir /var/cache/private
%ghost %attr(0700,root,root) %dir /var/lib/private
%ghost %dir /var/lib/private/systemd
%ghost %dir /var/lib/private/systemd/journal-upload
%ghost /var/lib/private/systemd/journal-upload/state
%ghost %dir /var/lib/systemd/timesync
%ghost /var/lib/systemd/timesync/clock
%ghost %dir /var/lib/systemd/backlight
%ghost /var/lib/systemd/catalog/database
%ghost %dir /var/lib/systemd/coredump
%ghost /var/lib/systemd/journal-upload
%ghost %dir /var/lib/systemd/linger
%ghost /var/lib/systemd/random-seed
%ghost %dir /var/lib/systemd/rfkill
%ghost %dir /var/log/journal
%ghost %dir /var/log/journal/remote
%ghost %attr(0700,root,root) %dir /var/log/private
EOF

%check
%meson_test

#############################################################################################

%include %{SOURCE1}

%pre
getent group cdrom &>/dev/null || groupadd -r -g 11 cdrom &>/dev/null || :
getent group utmp &>/dev/null || groupadd -r -g 22 utmp &>/dev/null || :
getent group tape &>/dev/null || groupadd -r -g 33 tape &>/dev/null || :
getent group dialout &>/dev/null || groupadd -r -g 18 dialout &>/dev/null || :
getent group input &>/dev/null || groupadd -r input &>/dev/null || :
getent group kvm &>/dev/null || groupadd -r -g 36 kvm &>/dev/null || :
getent group render &>/dev/null || groupadd -r render &>/dev/null || :
getent group systemd-journal &>/dev/null || groupadd -r -g 190 systemd-journal 2>&1 || :

getent group systemd-coredump &>/dev/null || groupadd -r systemd-coredump 2>&1 || :
getent passwd systemd-coredump &>/dev/null || useradd -r -l -g systemd-coredump -d / -s /sbin/nologin -c "systemd Core Dumper" systemd-coredump &>/dev/null || :

getent group systemd-network &>/dev/null || groupadd -r -g 192 systemd-network 2>&1 || :
getent passwd systemd-network &>/dev/null || useradd -r -u 192 -l -g systemd-network -d / -s /sbin/nologin -c "systemd Network Management" systemd-network &>/dev/null || :

getent group systemd-resolve &>/dev/null || groupadd -r -g 193 systemd-resolve 2>&1 || :
getent passwd systemd-resolve &>/dev/null || useradd -r -u 193 -l -g systemd-resolve -d / -s /sbin/nologin -c "systemd Resolver" systemd-resolve &>/dev/null || :

%post
systemd-machine-id-setup &>/dev/null || :
systemctl daemon-reexec &>/dev/null || :
journalctl --update-catalog &>/dev/null || :
systemd-tmpfiles --create &>/dev/null || :

# create /var/log/journal only on initial installation,
# and only if it's writable (it won't be in rpm-ostree).
if [ $1 -eq 1 ] && [ -w %{_localstatedir} ]; then
    mkdir -p %{_localstatedir}/log/journal
fi

# Make sure new journal files will be owned by the "systemd-journal" group
chgrp systemd-journal /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2>/dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2>/dev/null` &>/dev/null || :
chmod g+s /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2>/dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2>/dev/null` &>/dev/null || :

# Apply ACL to the journal directory
setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/ &>/dev/null || :

# We reset the enablement of all services upon initial installation
# https://bugzilla.redhat.com/show_bug.cgi?id=1118740#c23
# This will fix up enablement of any preset services that got installed
# before systemd due to rpm ordering problems:
# https://bugzilla.redhat.com/show_bug.cgi?id=1647172
if [ $1 -eq 1 ] ; then
        systemctl preset-all &>/dev/null || :
fi

%preun
if [ $1 -eq 0 ] ; then
        systemctl disable --quiet \
                remote-fs.target \
                getty@.service \
                serial-getty@.service \
                console-getty.service \
                debug-shell.service \
                systemd-readahead-replay.service \
                systemd-readahead-collect.service \
                systemd-networkd.service \
                systemd-networkd-wait-online.service \
                systemd-resolved.service \
                >/dev/null || :

        rm -f /etc/systemd/system/default.target &>/dev/null || :
fi

%post libs
%{?ldconfig}

function mod_nss() {
    if [ -f "$1" ] ; then
        # sed-fu to add myhostname to hosts line
        grep -E -q '^hosts:.* myhostname' "$1" ||
        sed -i.bak -e '
                /^hosts:/ !b
                /\<myhostname\>/ b
                s/[[:blank:]]*$/ myhostname/
                ' "$1" &>/dev/null || :

        # Add nss-systemd to passwd and group
        grep -E -q '^(passwd|group):.* systemd' "$1" ||
        sed -i.bak -r -e '
                s/^(passwd|group):(.*)/\1: \2 systemd/
                ' "$1" &>/dev/null || :
    fi
}

FILE="$(readlink /etc/nsswitch.conf || echo /etc/nsswitch.conf)"
if [ "$FILE" = "/etc/authselect/nsswitch.conf" ] && authselect check &>/dev/null; then
        mod_nss "/etc/authselect/user-nsswitch.conf"
        authselect apply-changes &> /dev/null || :
else
        mod_nss "$FILE"
        # also apply the same changes to user-nsswitch.conf to affect
        # possible future authselect configuration
        mod_nss "/etc/authselect/user-nsswitch.conf"
fi

# check if nobody or nfsnobody is defined
export SYSTEMD_NSS_BYPASS_SYNTHETIC=1
if getent passwd nfsnobody &>/dev/null; then
   test -f /etc/systemd/dont-synthesize-nobody || {
       echo 'Detected system with nfsnobody defined, creating /etc/systemd/dont-synthesize-nobody'
       mkdir -p /etc/systemd || :
       : >/etc/systemd/dont-synthesize-nobody || :
   }
elif getent passwd nobody 2>/dev/null | grep -v 'nobody:[x*]:65534:65534:.*:/:/sbin/nologin' &>/dev/null; then
   test -f /etc/systemd/dont-synthesize-nobody || {
       echo 'Detected system with incompatible nobody defined, creating /etc/systemd/dont-synthesize-nobody'
       mkdir -p /etc/systemd || :
       : >/etc/systemd/dont-synthesize-nobody || :
   }
fi

%{?ldconfig:%postun libs -p %ldconfig}

%global udev_services systemd-udev{d,-settle,-trigger}.service systemd-udevd-{control,kernel}.socket systemd-timesyncd.service

%pre udev
getent group systemd-timesync &>/dev/null || groupadd -r systemd-timesync 2>&1 || :
getent passwd systemd-timesync &>/dev/null || useradd -r -l -g systemd-timesync -d / -s /sbin/nologin -c "systemd Time Synchronization" systemd-timesync &>/dev/null || :

%post udev
# Move old stuff around in /var/lib
mv %{_localstatedir}/lib/random-seed %{_localstatedir}/lib/systemd/random-seed &>/dev/null
mv %{_localstatedir}/lib/backlight %{_localstatedir}/lib/systemd/backlight &>/dev/null
if [ -L %{_localstatedir}/lib/systemd/timesync ]; then
    rm %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/private/systemd/timesync %{_localstatedir}/lib/systemd/timesync
fi
if [ -f %{_localstatedir}/lib/systemd/clock ] ; then
    mkdir -p %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/systemd/clock %{_localstatedir}/lib/systemd/timesync/.
fi

udevadm hwdb --update &>/dev/null
%systemd_post %udev_services
/usr/lib/systemd/systemd-random-seed save 2>&1

# Replace obsolete keymaps
# https://bugzilla.redhat.com/show_bug.cgi?id=1151958
grep -q -E '^KEYMAP="?fi-latin[19]"?' /etc/vconsole.conf 2>/dev/null &&
    sed -i.rpm.bak -r 's/^KEYMAP="?fi-latin[19]"?/KEYMAP="fi"/' /etc/vconsole.conf || :

%preun udev
%systemd_preun %udev_services

%postun udev
# Only restart systemd-udev, to run the upgraded dameon.
# Others are either oneshot services, or sockets, and restarting them causes issues (#1378974)
%systemd_postun_with_restart systemd-udevd.service

%pre journal-remote
getent group systemd-journal-remote &>/dev/null || groupadd -r systemd-journal-remote 2>&1 || :
getent passwd systemd-journal-remote &>/dev/null || useradd -r -l -g systemd-journal-remote -d %{_localstatedir}/log/journal/remote -s /sbin/nologin -c "Journal Remote" systemd-journal-remote &>/dev/null || :

%post journal-remote
%systemd_post systemd-journal-gatewayd.socket systemd-journal-gatewayd.service
%systemd_post systemd-journal-remote.socket systemd-journal-remote.service
%systemd_post systemd-journal-upload.service
%firewalld_reload

%preun journal-remote
%systemd_preun systemd-journal-gatewayd.socket systemd-journal-gatewayd.service
%systemd_preun systemd-journal-remote.socket systemd-journal-remote.service
%systemd_preun systemd-journal-upload.service
if [ $1 -eq 1 ] ; then
    if [ -f %{_localstatedir}/lib/systemd/journal-upload/state -a ! -L %{_localstatedir}/lib/systemd/journal-upload ] ; then
        mkdir -p %{_localstatedir}/lib/private/systemd/journal-upload
        mv %{_localstatedir}/lib/systemd/journal-upload/state %{_localstatedir}/lib/private/systemd/journal-upload/.
        rmdir %{_localstatedir}/lib/systemd/journal-upload || :
    fi
fi

%postun journal-remote
%systemd_postun_with_restart systemd-journal-gatewayd.service
%systemd_postun_with_restart systemd-journal-remote.service
%systemd_postun_with_restart systemd-journal-upload.service
%firewalld_reload

%global _docdir_fmt %{name}

%files -f %{name}.lang -f .file-list-rest
%doc %{_pkgdocdir}
%exclude %{_pkgdocdir}/LICENSE.*
%license LICENSE.GPL2 LICENSE.LGPL2.1
%ghost %dir %attr(0755,-,-) /etc/systemd/system/basic.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/bluetooth.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/default.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/getty.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/graphical.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/local-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/machines.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/multi-user.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/network-online.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/printer.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/remote-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sockets.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sysinit.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/system-update.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/timers.target.wants
%ghost %dir %attr(0755,-,-) /var/lib/rpm-state/systemd

%files libs -f .file-list-libs
%license LICENSE.LGPL2.1

%files pam -f .file-list-pam

%files rpm-macros -f .file-list-rpm-macros

%files devel -f .file-list-devel

%files udev -f .file-list-udev

%files container -f .file-list-container

%files journal-remote -f .file-list-remote

%files tests -f .file-list-tests

%changelog
* Sat Feb  9 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241~rc2-2
- Turn LTO back on

* Tue Feb  5 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241~rc2-1
- Update to latest release -rc2

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Yu Watanabe <watanabe.yu@gmail.com> - 241~rc1-2
- Backport a patch for kernel-install

* Sat Jan 26 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241~rc1-1
- Update to latest release -rc1

* Tue Jan 15 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-6.gitf02b547
- Add a work-around for #1663040

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org>
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jan 11 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-4.gitf02b547
- Add a work-around for selinux issue on live images (#1663040)

* Fri Jan 11 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-3.gitf02b547
- systemd-journald and systemd-journal-remote reject entries which
  contain too many fields (CVE-2018-16865, #1664973) and set limits on the
  process' command line length (CVE-2018-16864, #1664972)
- $DBUS_SESSION_BUS_ADDRESS is again exported by pam_systemd (#1662857)
- A fix for systemd-udevd crash (#1662303)

* Sat Dec 22 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-2
- Add two more patches that revert recent udev changes

* Fri Dec 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-1
- Update to latest release
  See https://github.com/systemd/systemd/blob/master/NEWS for the list of changes.

* Mon Dec 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-10.git9f3aed1
- Hibernation checks for resume= are rescinded (#1645870)
- Various patches:
  - memory issues in logind, networkd, journald (#1653068), sd-device, etc.
  - Adaptations for newer meson, lz4, kernel
  - Fixes for misleading bugs in documentation
- net.ipv4.conf.all.rp_filter is changed from 1 to 2

* Thu Nov 29 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
- Adjust scriptlets to modify /etc/authselect/user-nsswitch.conf
  (see https://github.com/pbrezina/authselect/issues/77)
- Drop old scriptlets for nsswitch.conf modifications for nss-mymachines and nss-resolve

* Sun Nov 18 2018 Alejandro Domínguez Muñoz <adomu@net-c.com>
- Remove link creation for rsyslog.service

* Thu Nov  8 2018 Adam Williamson <awilliam@redhat.com> - 239-9.git9f3aed1
- Go back to using systemctl preset-all in %post (#1647172, #1118740)

* Mon Nov  5 2018 Adam Williamson <awilliam@redhat.com> - 239-8.git9f3aed1
- Requires(post) openssl-libs to fix live image build machine-id issue
  See: https://pagure.io/dusty/failed-composes/issue/960

* Mon Nov  5 2018 Yu Watanabe <watanabe.yu@gmail.com>
- Set proper attributes to private directories

* Fri Nov  2 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-7.git9f3aed1
- Split out the rpm macros into systemd-rpm-macros subpackage (#1645298)

* Sun Oct 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-6.git9f3aed1
- Fix a local vulnerability from a race condition in chown-recursive (CVE-2018-15687, #1639076)
- Fix a local vulnerability from invalid handling of long lines in state deserialization (CVE-2018-15686, #1639071)
- Fix a remote vulnerability in DHCPv6 in systemd-networkd (CVE-2018-15688, #1639067)
- The DHCP server is started only when link is UP
- DHCPv6 prefix delegation is improved
- Downgrade logging of various messages and add loging in other places
- Many many fixes in error handling and minor memory leaks and such
- Fix typos and omissions in documentation
- Typo in %%_environmnentdir rpm macro is fixed (with backwards compatiblity preserved)
- Matching by MACAddress= in systemd-networkd is fixed
- Creation of user runtime directories is improved, and the user
  manager is only stopped after 10 s after the user logs out (#1642460 and other bugs)
- systemd units systemd-timesyncd, systemd-resolved, systemd-networkd are switched back to use DynamicUser=0
- Aliases are now resolved when loading modules from pid1. This is a (redundant) fix for a brief kernel regression.
- "systemctl --wait start" exits immediately if no valid units are named
- zram devices are not considered as candidates for hibernation
- ECN is not requested for both in- and out-going connections (the sysctl overide for net.ipv4.tcp_ecn is removed)
- Various smaller improvements to unit ordering and dependencies
- generators are now called with the manager's environment
- Handling of invalid (intentionally corrupt) dbus messages is improved, fixing potential local DOS avenues
- The target of symlinks links in .wants/ and .requires/ is now ignored. This fixes an issue where
  the unit file would sometimes be loaded from such a symlink, leading to non-deterministic unit contents.
- Filtering of kernel threads is improved. This fixes an issues with newer kernels where hybrid kernel/user
  threads are used by bpfilter.
- "noresume" can be used on the kernel command line to force normal boot even if a hibernation images is present
- Hibernation is not advertised if resume= is not present on the kernenl command line
- Hibernation/Suspend/... modes can be disabled using AllowSuspend=,
  AllowHibernation=, AllowSuspendThenHibernate=, AllowHybridSleep=
- LOGO= and DOCUMENTATION_URL= are documented for the os-release file
- The hashmap mempool is now only used internally in systemd, and is disabled for external users of the systemd libraries
- Additional state is serialized/deserialized when logind is restarted, fixing the handling of user objects
- Catalog entries for the journal are improved (#1639482)
- If suspend fails, the post-suspend hooks are still called.
- Various build issues on less-common architectures are fixed

* Wed Oct  3 2018 Jan Synáček <jsynacek@redhat.com> - 239-5
- Fix meson using -Ddebug, which results in FTBFS
- Fix line_begins() to accept word matching full string (#1631840)

* Mon Sep 10 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-4
- Move /etc/yum/protected.d/systemd.conf to /etc/dnf/ (#1626969)

* Wed Jul 18 2018 Terje Rosten <terje.rosten@ntnu.no> - 239-3
- Ignore return value from systemd-binfmt in scriptlet (#1565425)

* Sun Jul 15 2018 Filipe Brandenburger <filbranden@gmail.com>
- Override systemd-user PAM config in install and not prep

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
- Rebuild for Python 3.7 again

* Fri Jun 22 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-1
- Update to latest version, mostly bug fixes and new functionality,
  very little breaking changes. See
  https://github.com/systemd/systemd/blob/v239/NEWS for details.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com>
- Rebuilt for Python 3.7

* Fri May 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-8.git0e0aa59
- Backport a number of patches (documentation, hwdb updates)
- Fixes for tmpfiles 'e' entries
- systemd-networkd crashes
- XEN virtualization detection on hyper-v
- Avoid relabelling /sys/fs/cgroup if not needed (#1576240)

* Wed Apr 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-7.fc28.1
- Allow fake Delegate= setting on slices (#1568594)

* Wed Mar 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-7
- Move udev transfiletriggers to the right package, fix quoting

* Tue Mar 27 2018 Colin Walters <walters@verbum.org> - 238-6
- Use shell for triggers; see https://github.com/systemd/systemd/pull/8550
  This fixes compatibility with rpm-ostree.

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-5
- Backport patch to revert inadvertent change of "predictable" interface name (#1558027)

* Fri Mar 16 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-4
- Do not close dbus connection during dbus reload call (#1554578)

* Wed Mar  7 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-3
- Revert the patches for GRUB BootLoaderSpec support
- Add patch for /etc/machine-id creation (#1552843)

* Tue Mar  6 2018 Yu Watanabe <watanabe.yu@gmail.com> - 238-2
- Fix transfiletrigger script (#1551793)

* Mon Mar  5 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-1
- Update to latest version
- This fixes a hard-to-trigger potential vulnerability (CVE-2018-6954)
- New transfiletriggers are installed for udev hwdb and rules, the journal
  catalog, sysctl.d, binfmt.d, sysusers.d, tmpfiles.d.

* Tue Feb 27 2018 Javier Martinez Canillas <javierm@redhat.com> - 237-7.git84c8da5
- Add patch to install kernel images for GRUB BootLoaderSpec support

* Sat Feb 24 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-6.git84c8da5
- Create /etc/systemd in %%post libs if necessary (#1548607)

* Fri Feb 23 2018 Adam Williamson <awilliam@redhat.com> - 237-5.git84c8da5
- Use : not touch to create file in -libs %%post

* Thu Feb 22 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 237-4.git84c8da5
- Add coreutils dep for systemd-libs %%post
- Add patch to typecast USB IDs to avoid compile failure

* Wed Feb 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-3.git84c8da5
- Update some patches for test skipping that were updated upstream
  before merging
- Add /usr/lib/systemd/purge-nobody-user — a script to check if nobody is defined
  correctly and possibly replace existing mappings

* Tue Feb 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-2.gitdff4849
- Backport a bunch of patches, most notably for the journal and various
  memory issues. Some minor build fixes.
- Switch to new ldconfig macros that do nothing in F28+
- /etc/systemd/dont-synthesize-nobody is created in %%post if nfsnobody
  or nobody users are defined (#1537262)

* Fri Feb  9 2018 Zbigniew Jędrzejeweski-Szmek <zbyszek@in.waw.pl> - 237-1.git78bd769
- Update to first stable snapshot (various minor memory leaks and misaccesses,
  some documentation bugs, build fixes).

* Sun Jan 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-1
- Update to latest version

* Sun Jan 21 2018 Björn Esser <besser82@fedoraproject.org> - 236-4.git3e14c4c
- Add patch to include <crypt.h> if needed

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 236-3.git3e14c4c
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 236-2.git23e14c4
- Backport a bunch of bugfixes from upstream (#1531502, #1531381, #1526621
  various memory corruptions in systemd-networkd)
- /dev/kvm is marked as a static node which fixes permissions on s390x
  and ppc64 (#1532382)

* Fri Dec 15 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 236-1
- Update to latest version

* Mon Dec 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-5.git4a0e928
- Update to latest git snapshot, do not build for realz
- Switch to libidn2 again (#1449145)

* Tue Nov 07 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-4
- Rebuild for cryptsetup-2.0.0-0.2.fc28

* Wed Oct 25 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-3
- Backport a bunch of patches, including LP#172535

* Wed Oct 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-2
- Patches for cryptsetup _netdev

* Fri Oct  6 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-1
- Update to latest version

* Tue Sep 26 2017 Nathaniel McCallum <npmccallum@redhat.com> - 234-8
- Backport /etc/crypttab _netdev feature from upstream

* Thu Sep 21 2017 Michal Sekletar <msekleta@redhat.com> - 234-7
- Make sure to remove all device units sharing the same sysfs path (#1475570)

* Mon Sep 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-6
- Bump xslt recursion limit for libxslt-1.30

* Mon Jul 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-5
- Backport more patches (#1476005, hopefully #1462378)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-3
- Fix x-systemd.timeout=0 in /etc/fstab (#1462378)
- Minor patches (memleaks, --help fixes, seccomp on arm64)

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-2
- Create kvm group (#1431876)

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-1
- Latest release

* Sat Jul  1 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-7.git74d8f1c
- Update to snapshot
- Build with meson again

* Tue Jun 27 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-6
- Fix an out-of-bounds write in systemd-resolved (CVE-2017-9445)

* Fri Jun 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-5.gitec36d05
- Update to snapshot version, build with meson

* Thu Jun 15 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-4
- Backport a bunch of small fixes (memleaks, wrong format strings,
  man page clarifications, shell completion)
- Fix systemd-resolved crash on crafted DNS packet (CVE-2017-9217, #1455493)
- Fix systemd-vconsole-setup.service error on systems with no VGA console (#1272686)
- Drop soft-static uid for systemd-journal-gateway
- Use ID from /etc/os-release as ntpvendor

* Thu Mar 16 2017 Michal Sekletar <msekleta@redhat.com> - 233-3
- Backport bugfixes from upstream
- Don't return error when machinectl couldn't figure out container IP addresses (#1419501)

* Thu Mar  2 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-2
- Fix installation conflict with polkit

* Thu Mar  2 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-1
- New upstream release (#1416201, #1405439, #1420753, many others)
- New systemd-tests subpackage with "installed tests"

* Thu Feb 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-15
- Add %%ghost %%dir entries for .wants dirs of our targets (#1422894)

* Tue Feb 14 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-14
- Ignore the hwdb parser test

* Tue Feb 14 2017 Jan Synáček <jsynacek@redhat.com> - 232-14
- machinectl fails when virtual machine is running (#1419501)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 232-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-12
- Backport patch for initrd-switch-root.service getting killed (#1414904)
- Fix sd-journal-gatewayd -D, --trust, and COREDUMP_CONTAINER_CMDLINE
  extraction by sd-coredump.

* Sun Jan 29 2017 zbyszek <zbyszek@in.waw.pl> - 232-11
- Backport a number of patches (#1411299, #1413075, #1415745,
                                ##1415358, #1416588, #1408884)
- Fix various memleaks and unitialized variable access
- Shell completion enhancements
- Enable TPM logging by default (#1411156)
- Update hwdb (#1270124)

* Thu Jan 19 2017 Adam Williamson <awilliam@redhat.com> - 232-10
- Backport fix for boot failure in initrd-switch-root (#1414904)

* Wed Jan 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-9
- Add fake dependency on systemd-pam to systemd-devel to ensure systemd-pam
  is available as multilib (#1414153)

* Tue Jan 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-8
- Fix buildsystem to check for lz4 correctly (#1404406)

* Wed Jan 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-7
- Various small tweaks to scriplets

* Sat Jan 07 2017 Kevin Fenzi <kevin@scrye.com> - 232-6
- Fix scriptlets to never fail in libs post

* Fri Jan 06 2017 Kevin Fenzi <kevin@scrye.com> - 232-5
- Add patch from Michal Schmidt to avoid process substitution (#1392236)

* Sun Nov  6 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-4
- Rebuild (#1392236)

* Fri Nov  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-3
- Make /etc/dbus-1/system.d directory non-%%ghost

* Fri Nov  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-2
- Fix kernel-install (#1391829)
- Restore previous systemd-user PAM config (#1391836)
- Move journal-upload.conf.5 from systemd main to journal-remote subpackage (#1391833)
- Fix permissions on /var/lib/systemd/journal-upload (#1262665)

* Thu Nov  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-1
- Update to latest version (#998615, #1181922, #1374371, #1390704, #1384150, #1287161)
- Add %%{_isa} to Provides on arch-full packages (#1387912)
- Create systemd-coredump user in %%pre (#1309574)
- Replace grubby patch with a short-circuiting install.d "plugin"
- Enable nss-systemd in the passwd, group lines in nsswith.conf
- Add [!UNAVAIL=return] fallback after nss-resolve in hosts line in nsswith.conf
- Move systemd-nspawn man pages to the right subpackage (#1391703)

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

* Wed Aug 03 2016 Adam Williamson <awilliam@redhat.com> - 231-3
- Revert preset-all change, it broke stuff (#1363858)

* Wed Jul 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-2
- Call preset-all on initial installation (#1118740)
- Fix botched Recommends for libxkbcommon

* Tue Jul 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-1
- Update to latest version

* Wed Jun  8 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 230-3
- Update to latest git snapshot (fixes for systemctl set-default,
  polkit lingering policy, reversal of the framebuffer rules,
  unaligned access fixes, fix for StartupBlockIOWeight-over-dbus).
  Those changes are interspersed with other changes and new features
  (mostly in lldp, networkd, and nspawn). Some of those new features
  might not work, but I think that existing functionality should not
  be broken, so it seems worthwile to update to the snapshot.

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-2
- Remove systemd-compat-libs on upgrade

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-1
- New version
- Drop compat-libs
- Require libxkbcommon explictly, since the automatic dependency will
  not be generated anymore

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
- Remove ghosting for /etc/systemd/system/runlevel*.target, these
  targets are not configurable anymore in systemd upstream
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
