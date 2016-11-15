Name:	mkosi
Version: 1
Release: 1.fb1
Summary: Build Legacy-Free OS Images

License: LGPL 2.1
URL: https://github.com/systemd/mkosi/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
Source1: RPM-GPG-KEY-fedora-23-x86_64
Source2: RPM-GPG-KEY-fedora-24-x86_64
Source3: RPM-GPG-KEY-fedora-25-x86_64
Source4: RPM-GPG-KEY-fedora-26-x86_64

Requires: python35
Requires: arch-install-scripts
Requires: dnf
Requires: debootstrap
Requires: xz
Requires: btrfs-progs
Requires: dosfstools
Requires: e2fsprogs
Requires: systemd-container

Patch0: fix-mirror-for-Fedora-25-and-add-all-keys.patch

%description
A fancy wrapper around dnf --installroot, debootstrap and pacstrap, that may generate disk images with a number of bells and whistles.

%prep
%setup -q
%patch0 -p1

%build
sed -i mkosi -e 's:/usr/bin/python3:/usr/bin/python35:'

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 mkosi %{buildroot}%{_bindir}/mkosi
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m 0644 %SOURCE1 %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-23-x86_64
install -m 0644 %SOURCE2 %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-24-x86_64
install -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-25-x86_64
install -m 0644 %SOURCE4 %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-26-x86_64

%files
%{_bindir}/mkosi
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-23-x86_64
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-24-x86_64
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-25-x86_64
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-26-x86_64

%changelog
* Mon Nov 7 2016 Davide Cavalca <dcavalca@fb.com> - 1-1.fb1
- first upstream release
- add GPG keys for Fedora 23, 25, 26
- fix mirror for Fedora 25 and improve keys handling (PR#37)

* Fri Nov 4 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb3
- switch python dependency to use backported python35 package

* Fri Sep 2 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb2
- rebase on 04e70cf6106ce4da440798fd70ef74728ddf3285
- add depends on arch-install-scripts now that it's available

* Thu Sep 1 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb1
- initial package based on fb3ec53a73dd84281c1fae50036dac2ccf7448a3
- add internal patches
- add GPG key for Fedora 24
- depend on fbcode python and fix shebang accordingly as this needs at least 3.5
