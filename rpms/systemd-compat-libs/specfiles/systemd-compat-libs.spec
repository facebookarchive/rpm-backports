# Meson settings
%global _vpath_srcdir .
%global _vpath_builddir %{_target_platform}
%global __global_cflags  %{optflags}
%global __global_cxxflags  %{optflags}
%global __global_fflags  %{optflags} -I%_fmoddir
%global __global_fcflags %{optflags} -I%_fmoddir
%global __global_ldflags -Wl,-z,relro %{_hardened_ldflags}
%global __meson_wrap_mode default

#global commit d9b85f3d1a1954598414cce83e41b5aa9222ad6f
#global systemd_commit 7f56c26d1041e686efa72b339250a98fb6ee8f00
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}
%{?commit:%global systemd_shortcommit %(c=%{systemd_commit}; echo ${c:0:7})}

Name:           systemd-compat-libs
Url:            https://github.com/facebookincubator/systemd-compat-libs
Version:        246.1
Release:        1.fb7
# For a breakdown of the licensing, see README
License:        LGPLv2+
Summary:        Compatibility libraries for systemd

%global stable 1
%global systemd_version %(c=%{version}; echo ${c}|tr '~' '-')

%if 0%{?facebook}
%if 0%{?el7}
### The version of meson and redhat-rpm-config is not in sync in C7.
### Copied from the 'redhat-rpm-config-123-1' version of /usr/lib/rpm/redhat/macros
### to support the building of systemd via meson that uses the
### set_build_flags macro.
%global _ld_symbols_flags              %{?_strict_symbol_defs_build:-Wl,-z,defs}

#==============================================================================
# ---- compiler flags.

# C compiler flags.  This is traditionally called CFLAGS in makefiles.
# Historically also available as %%{optflags}, and %%build sets the
# environment variable RPM_OPT_FLAGS to this value.
%global build_cflags %{optflags}

# C++ compiler flags.  This is traditionally called CXXFLAGS in makefiles.
%global build_cxxflags %{optflags}

# Fortran compiler flags.  Makefiles use both FFLAGS and FCFLAGS as
# the corresponding variable names.
%global build_fflags %{optflags} -I%{_fmoddir}

# Link editor flags.  This is usually called LDFLAGS in makefiles.
# (Some makefiles use LFLAGS instead.)  The default value assumes that
# the flags, while intended for ld, are still passed through the gcc
# compiler driver.  At the beginning of %%build, the environment
# variable RPM_LD_FLAGS to this value.
%global build_ldflags -Wl,-z,relro %{_ld_symbols_flags} %{_hardened_ldflags}

# Expands to shell code to seot the compiler/linker environment
# variables CFLAGS, CXXFLAGS, FFLAGS, FCFLAGS, LDFLAGS if they have
# not been set already.  RPM_OPT_FLAGS and RPM_LD_FLAGS have already
# been set implicitly at the start of the %%build section.
%global set_build_flags \
  CFLAGS="${CFLAGS:-%{build_cflags}}" ; export CFLAGS ; \
  CXXFLAGS="${CXXFLAGS:-%{build_cxxflags}}" ; export CXXFLAGS ; \
  FFLAGS="${FFLAGS:-%{build_fflags}}" ; export FFLAGS ; \
  FCFLAGS="${FCFLAGS:-%{build_fflags}}" ; export FCFLAGS ; \
  LDFLAGS="${LDFLAGS:-%{build_ldflags}}" ; export LDFLAGS;

### Copied from the rpm-4.14.2-36 version of /usr/lib/rpm/platform/x86_64-linux/macros
### to support the building of systemd via meson that uses the
### _smp_build_ncpus macro
%global _smp_build_ncpus %([ -z "$RPM_BUILD_NCPUS" ] \\\
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \\\
        ncpus_max=%{?_smp_ncpus_max}; \\\
        if [ -n "$ncpus_max" ] && [ "$ncpus_max" -gt 0 ] && [ "$RPM_BUILD_NCPUS" -gt "$ncpus_max" ]; then RPM_BUILD_NCPUS="$ncpus_max"; fi; \\\
        echo "$RPM_BUILD_NCPUS";)

%global _smp_mflags -j%{_smp_build_ncpus}
%endif
%endif

# The systemd-stable versions don't follow the scheme we use for
# systemd-compat-libs so define the actual github version here.
# This is the same as systemd_version if we key off regular (not stable) systemd.
%global github_version 246

%if %{defined commit}
Source0:        https://github.com/facebookincubator/systemd-compat-libs/archive/%{?commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/facebookincubator/systemd-compat-libs/archive/v%{github_version}/%{name}-%{github_version}.tar.gz
%endif
%if %{defined systemd_commit}
Source1:        https://github.com/systemd/systemd%{?stable:-stable}/archive/%{?systemd_commit}/systemd-%{systemd_shortcommit}.tar.gz
%else
%if 0%{?stable}
Source1:        https://github.com/systemd/systemd-stable/archive/v%{systemd_version}/systemd-%{systemd_version}.tar.gz
%else
Source1:        https://github.com/systemd/systemd/archive/v%{systemd_version}/systemd-%{systemd_version}.tar.gz
%endif
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
BuildRequires:  python3
%if %{defined systemd_commit} || 0%{?stable}
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
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and auxiliary files for developing applications linking
to systemd-compat-libs.

%prep
%autosetup -n %{?commit:%{name}-%{commit}}%{!?commit:%{name}-%{github_version}} -p1 -Sgit
mkdir -p subprojects/packagecache
cp -p %SOURCE1 subprojects/packagecache/

%if %{defined systemd_commit}
sed -i meson.build -e "s/version : '[0-9]*'/version : '%{systemd_version}'/"
cat > subprojects/systemd.wrap <<EOF
[wrap-file]
directory = systemd-%{systemd_commit}
source_url = https://github.com/systemd/systemd%{?stable:-stable}/archive/%{systemd_commit}/systemd-%{systemd_shortcommit}.tar.gz
source_filename = systemd-%{systemd_shortcommit}.tar.gz
source_hash = $(sha256sum %SOURCE1 | awk '{print $1}')
EOF
%else
%if 0%{?stable}
sed -i meson.build -e "s/version : '[0-9]*'/version : '%{systemd_version}'/"
cat > subprojects/systemd.wrap <<EOF
[wrap-file]
directory = systemd-stable-%{systemd_version}
source_url = https://github.com/systemd/systemd-stable/archive/v%{systemd_version}/systemd-%{systemd_version}.tar.gz
source_filename = systemd-%{systemd_version}.tar.gz
source_hash = $(sha256sum %SOURCE1 | awk '{print $1}')
EOF
%endif
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
* Tue Feb  16 2021 Anita Zhang <anitazha@fb.com> - 246.1-1.fb7
- Bump version to match systemd packages

* Mon Jan  25 2021 Anita Zhang <anitazha@fb.com> - 246.1-1.fb6
- Bump version to match systemd packages
 
* Thu Nov  19 2020 Chris Down <cdown@fb.com> - 246.1-1.fb5
- Bump version to match systemd packages

* Thu Nov  19 2020 Chris Down <cdown@fb.com> - 246.1-1.fb4
- Bump version to match systemd packages

* Fri Sep  18 2020 Anita Zhang <anitazha@fb.com> - 246.1-1.fb3
- Bump version to match systemd packages

* Tue Aug  18 2020 Anita Zhang <anitazha@fb.com> - 246.1-1.fb2
- Bump version to match systemd packages

* Mon Aug  17 2020 Anita Zhang <anitazha@fb.com> - 246.1-1.fb1
- New upstream release

* Fri Jun  5 2020 Anita Zhang <anitazha@fb.com> - 245.5-2.fb3
- Bump version to match systemd packages

* Thu Jun  4 2020 Anita Zhang <anitazha@fb.com> - 245.5-2.fb2
- Bump version to match systemd packages

* Thu Apr 30 2020 Anita Zhang <anitazha@fb.com> - 245.5-2.fb1
- New upstream release

* Thu Mar 26 2020 Andrew Gallagher <agallagher@fb.com> - 244-2.fb4
- Bump version to match systemd packages

* Thu Feb  6 2020 Anita Zhang <anitazha@fb.com> - 244-2.fb2
- Bump version to match systemd packages

* Thu Jan  9 2020 Anita Zhang <anitazha@fb.com> - 244-2.fb1
- New upstream release

* Thu Oct 31 2019 Davide Cavalca <dcavalca@fb.com> - 243-2.fb3
- Bump version to match systemd packages

* Thu Oct  3 2019 Davide Cavalca <dcavalca@fb.com> - 243-2.fb2
- Bump version to match systemd packages

* Fri Sep 27 2019 Davide Cavalca <dcavalca@fb.com> - 243-2.fb1
- New upstream release

* Wed Aug 7 2019 Anita Zhang <anitazha@fb.com> - 242-2.fb4
- Bump version to match systemd packages

* Thu Jul 18 2019 Anita Zhang <anitazha@fb.com> - 242-2.fb3
- Bump version to match systemd packages

* Thu Jun 20 2019 Anita Zhang <anitazha@fb.com> - 242-2.fb2
- Bump version to match systemd packages

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
