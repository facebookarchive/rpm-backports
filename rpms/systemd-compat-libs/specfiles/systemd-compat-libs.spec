# Meson settings
%global _vpath_srcdir .
%global _vpath_builddir %{_target_platform}
%global __global_cflags  %{optflags}
%global __global_cxxflags  %{optflags}
%global __global_fflags  %{optflags} -I%_fmoddir
%global __global_fcflags %{optflags} -I%_fmoddir
%global __global_ldflags -Wl,-z,relro %{_hardened_ldflags}
%global __meson_wrap_mode default

#global commit ad47606e6ac9f4ef3451369a4c3b1ba2b60ef16d
#global systemd_commit f02b5472c6f0c41e5dc8dc2c84590866baf937ff
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}
%{?commit:%global systemd_shortcommit %(c=%{systemd_commit}; echo ${c:0:7})}

Name:           systemd-compat-libs
Url:            https://github.com/facebookincubator/systemd-compat-libs
Version:        242
Release:        2.fb1
# For a breakdown of the licensing, see README
License:        LGPLv2+
Summary:        Compatibility libraries for systemd

%global github_version %(c=%{version}; echo ${c}|tr '~' '-')

%if %{defined commit}
Source0:        https://github.com/facebookincubator/systemd-compat-libs/archive/%{?commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/facebookincubator/systemd-compat-libs/archive/v%{github_version}/%{name}-%{github_version}.tar.gz
%endif
%if %{defined systemd_commit}
Source1:        https://github.com/systemd/systemd/archive/%{?systemd_commit}/systemd-%{systemd_shortcommit}.tar.gz
%else
Source1:        https://github.com/systemd/systemd/archive/v%{github_version}/systemd-%{github_version}.tar.gz
%endif

BuildRequires:  meson >= 0.47
BuildRequires:  git
BuildRequires:  m4
BuildRequires:  gperf
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  python34
%if %{defined systemd_commit}
BuildRequires:  coreutils
BuildRequires:  gawk
%endif
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
%autosetup -n %{?commit:%{name}%{?stable:-stable}-%{commit}}%{!?commit:%{name}%{?stable:-stable}-%{github_version}} -p1 -Sgit
mkdir -p subprojects/packagecache
cp -p %SOURCE1 subprojects/packagecache/

%if %{defined systemd_commit}
sed -i meson.build -e "s/version : '[0-9]*'/version : '%{github_version}'/"
cat > subprojects/systemd.wrap <<EOF
[wrap-file]
directory = systemd-%{systemd_commit}
source_url = https://github.com/systemd/systemd/archive/%{?systemd_commit}.tar.gz
source_filename = systemd-%{systemd_shortcommit}.tar.gz
source_hash = $(sha256sum %SOURCE1 | awk '{print $1}')
EOF
%endif

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
* Thu Apr 25 2019 Davide Cavalca <dcavalca@fb.com> - 242-2.fb1
- New upstream release

* Fri Mar 22 2019 Davide Cavalca <dcavalca@fb.com> - 241-1.fb2
- Bump version to match systemd packages

* Wed Feb 27 2019 Davide Cavalca <dcavalca@fb.com> - 241-1.fb1
- New upstream release
- Bump meson requirement to match systemd

* Wed Dec  5 2018 Davide Cavalca <dcavalca@fb.com> - 239-1.fb6
- Bump version to match systemd packages

* Fri Nov  2 2018 Davide Cavalca <dcavalca@fb.com> - 239-1.fb5
- Bump version to match systemd packages

* Fri Oct 12 2018 Davide Cavalca <dcavalca@fb.com> - 239-1.fb4
- Bump version to match systemd packages
- Add python34 to BuildRequires

* Mon Aug 27 2018 Davide Cavalca <dcavalca@fb.com> - 239-1.fb3
- Bump version to match systemd packages

* Wed Jul  4 2018 Davide Cavalca <dcavalca@fb.com> - 239-1.fb2
- Bump version to match systemd packages

* Mon Jun 25 2018 Davide Cavalca <dcavalca@fb.com> - 239-1.fb1
- New upstream release

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
