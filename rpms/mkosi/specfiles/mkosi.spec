Name:	mkosi
Version: 0.0.1
Release: 1.fb2
Summary: Build Legacy-Free OS Images

License: LGPL 2.1
URL: https://github.com/systemd/mkosi
Source0: mkosi
Source1: RPM-GPG-KEY-fedora-24-x86_64
Patch0: 0001-Fix-arch-mirror-selection.patch

Requires: fb-gcc-4.9-glibc-2.20-fb-python3-runtime
Requires: arch-install-scripts
Requires: dnf
Requires: debootstrap
Requires: xz
Requires: btrfs-progs
Requires: dosfstools
Requires: e2fsprogs
Requires: systemd-container

%description
A fancy wrapper around dnf --installroot, debootstrap and pacstrap, that may generate disk images with a number of bells and whistles.

%prep
cp %SOURCE0 .
%patch0 -p1

%build
sed -i mkosi -e 's:/usr/bin/python3:/usr/local/fbcode/gcc-4.9-glibc-2.20-fb/bin/python3.5:'

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 mkosi %{buildroot}%{_bindir}/mkosi
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m 0644 %SOURCE1 %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-24-x86_64

%files
%{_bindir}/mkosi
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-24-x86_64

%changelog
* Fri Sep 2 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb2
- rebase on 04e70cf6106ce4da440798fd70ef74728ddf3285
- add depends on arch-install-scripts now that it's available

* Thu Sep 1 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb1
- initial package based on fb3ec53a73dd84281c1fae50036dac2ccf7448a3
- add internal patches
- add GPG key for Fedora 24
- depend on fbcode python and fix shebang accordingly as this needs at least 3.5
