# Meson settings
%global _vpath_srcdir .
%global _vpath_builddir %{_target_platform}
%global __global_cflags  %{optflags}
%global __global_cxxflags  %{optflags}
%global __global_fflags  %{optflags} -I%_fmoddir
%global __global_fcflags %{optflags} -I%_fmoddir
%global __global_ldflags -Wl,-z,relro %{_hardened_ldflags}
%global __meson_wrap_mode default

Name:           systemd-compat-libs
Url:            https://github.com/facebookincubator/systemd-compat-libs
Version:        238
Release:        7.fb3
# For a breakdown of the licensing, see README
License:        LGPLv2+
Summary:        Compatibility libraries for systemd

Source0:        https://github.com/facebookincubator/systemd-compat-libs/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/systemd/systemd/archive/v%{version}.tar.gz#/systemd-%{version}.tar.gz
Source2:        https://github.com/facebookincubator/systemd-compat-libs/archive/raw/master/wrap-patches/systemd-%{version}-wrap-patch.tar.gz

BuildRequires:  meson >= 0.44
BuildRequires:  git
BuildRequires:  m4
BuildRequires:  gperf
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
Obsoletes:      system-compat-libs < %{version}-%{release}

%description
This is a standalone build of the compatibility libraries for systemd, 
which map library calls for systemd < 209 onto the new libsystemd.so 
provided by later versions. These libraries used to be shipped with 
systemd, but were removed upstream in v230. This project allows one 
to easily backport recent versions of systemd on distributions that 
originally shipped with versions < 230, such as CentOS 7.

%package devel
Summary:        Development headers for systemd-compat-libs
License:        LGPLv2+
Requires:       %{name}-compat-libs%{?_isa} = %{version}-%{release}

%description devel
Development headers and auxiliary files for developing applications linking
to systemd-compat-libs.

%prep
%setup -q
%autopatch -p1
mkdir -p subprojects/packagecache
cp -p %SOURCE1 subprojects/packagecache/
cp -p %SOURCE2 subprojects/packagecache/

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
%meson
%meson_build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
%meson_install

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libsystemd-daemon.so.*
%{_libdir}/libsystemd-login.so.*
%{_libdir}/libsystemd-journal.so.*
%{_libdir}/libsystemd-id128.so.*

%files devel
%{_libdir}/libsystemd-daemon.so
%{_libdir}/libsystemd-login.so
%{_libdir}/libsystemd-journal.so
%{_libdir}/libsystemd-id128.so
%{_libdir}/pkgconfig/libsystemd-daemon.pc
%{_libdir}/pkgconfig/libsystemd-login.pc
%{_libdir}/pkgconfig/libsystemd-journal.pc
%{_libdir}/pkgconfig/libsystemd-id128.pc

%changelog
* Wed May 16 2018 Davide Cavalca <dcavalca@fb.com> - 238-7.fb3
- Bump version to match systemd packages

* Tue May 15 2018 Davide Cavalca <dcavalca@fb.com> - 238-7.fb2
- Bump version to match systemd packages

* Thu Apr  5 2018 Davide Cavalca <dcavalca@fb.com> - 238-7.fb1
- New upstream release

* Mon Feb 26 2018 Davide Cavalca <dcavalca@fb.com> - 237-1.fb3
- Bump version to match systemd packages

* Thu Feb 22 2018 Davide Cavalca <dcavalca@fb.com> - 237-1.fb2
- Bump version to match systemd packages

* Mon Feb 12 2018 Davide Cavalca <dcavalca@fb.com> - 237-1.fb1
- New upstream release

* Mon Oct  9 2017 Davide Cavalca <dcavalca@fb.com> - 235-1.fb1
- New upstream release

* Tue Sep 19 2017 Davide Cavalca <dcavalca@fb.com> - 234-5.fb2
- Backport libraries versions fix from PR#1

* Fri Aug 18 2017 Davide Cavalca <dcavalca@fb.com> - 234-5.fb1
- Initial release
