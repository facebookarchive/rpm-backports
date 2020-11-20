Name:           mkosi
Version:        6
Release:        1.fb1%{?dist}
Summary:        Create legacy-free OS images

License:        LGPLv2+
URL:            https://github.com/systemd/mkosi
Source0:        https://github.com/systemd/mkosi/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if ! 0%{?facebook}
BuildRequires:  pip
%endif

Recommends:     dnf
Recommends:     debootstrap
Recommends:     arch-install-scripts
Recommends:     edk2-ovmf
Recommends:     gnupg
Recommends:     xz
Recommends:     tar
Recommends:     btrfs-progs
Recommends:     dosfstools
Recommends:     e2fsprogs
Recommends:     squashfs-tools
Recommends:     veritysetup
Recommends:     python3dist(argcomplete)

%description
A fancy wrapper around "dnf --installroot", "debootstrap" and
"pacstrap", that may generate disk images with a number of bells and
whistles.

Generated images are "legacy-free". This means only GPT disk labels
(and no MBR disk labels) are supported, and only systemd based images
may be generated. Moreover, for bootable images only EFI systems are
supported (not plain MBR/BIOS).

%prep
%autosetup -p1

%build
# no build required

%install
python3 -m pip install --root=%{buildroot} .

# Also install Fedora GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

%files
%license LICENSE
%doc README.md
%_bindir/mkosi
%{python3_sitelib}/mkosi/
%{python3_sitelib}/mkosi-%{version}-py*.egg-info/
%_mandir/man1/mkosi.1*

%check
# just a smoke test for syntax or import errors
%buildroot/usr/bin/mkosi --help

%changelog
* Thu Nov 19 2020 Anita Zhang <anitazha@fb.com> - 6-1.fb1
- Facebook rebuild
- Remove GPG keys

* Sat Oct  3 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6-1
- Update to latest version (#1884879)

* Tue May 26 2020 Davide Cavalca <dcavalca@fb.com> - 5-2.fb2
- Fix build after python package rename

* Wed Oct 02 2019 Davide Cavalca <dcavalca@fb.com> - 5-2.fb1
- Facebook rebuild
- Add Fedora 30, 31, 32 keys

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5-1
- Update to latest version

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Davide Cavalca <dcavalca@fb.com> - 4-2.fb3
- Add Fedora 29 GPG key
- Backport https://github.com/systemd/mkosi/pull/250

* Thu Feb 22 2018 Davide Cavalca <dcavalca@fb.com> - 4-2.fb2
- Move to python36
- Reenable smoketest

* Thu Feb 22 2018 Davide Cavalca <dcavalca@fb.com> - 4-2.fb1
- New upstream release
- Add Fedora 28 GPG key
- Disable smoketest as python35 doesn't seem to run in mock

* Sat Feb 10 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4-2
- Update to latest version (#1544123)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 7 2017 Davide Cavalca <dcavalca@fb.com> - 2-2.fb1
- Rebase over upstream packaging
- add GPG key for Fedora 27

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2-1
- Update to latest version (#1464285)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1-2
- Rebuild for Python 3.6

* Mon Nov 7 2016 Davide Cavalca <dcavalca@fb.com> - 1-1.fb1
- first upstream release
- add GPG keys for Fedora 23, 25, 26
- fix mirror for Fedora 25 and improve keys handling (PR#37)

* Fri Nov 4 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb3
- switch python dependency to use backported python35 package

* Thu Nov  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1-1
- Initial version

* Fri Sep 2 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb2
- rebase on 04e70cf6106ce4da440798fd70ef74728ddf3285
- add depends on arch-install-scripts now that it's available

* Thu Sep 1 2016 Davide Cavalca <dcavalca@fb.com> - 0.0.1-1.fb1
- initial package based on fb3ec53a73dd84281c1fae50036dac2ccf7448a3
- add internal patches
- add GPG key for Fedora 24
- depend on fbcode python and fix shebang accordingly as this needs at least 3.5
