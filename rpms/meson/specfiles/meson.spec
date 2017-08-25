%global libname mesonbuild
%if 0%{?rhel}
%global python3_pkgversion 34
%define rpmmacrodir %{_rpmconfigdir}/macros.d
%endif

Name:           meson
Version:        0.41.2
Release:        2.fb1%{?dist}
Summary:        High productivity build system

License:        ASL 2.0
URL:            http://mesonbuild.com/
Source0:        https://github.com/mesonbuild/meson/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
Obsoletes:      %{name}-gui < 0.31.0-3

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  ninja-build
# Various languages
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  gcc-objc
BuildRequires:  gcc-objc++
BuildRequires:  java-devel
BuildRequires:  mono-core mono-devel
BuildRequires:  rust
# No ldc as of RHEL7 and on non-ldc arches
%if ! 0%{?rhel} || 0%{?rhel} > 7
# Since the build is noarch, we can't use %ifarch
#%%ifarch %%{ldc_arches}
#BuildRequires:  ldc
#%%endif
%endif
# Various libs support
BuildRequires:  boost-devel
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  vala
# In recent versions it's merged into vala
%if (0%{?fedora} && 0%{?fedora} <= 24) || (0%{?rhel} && 0%{?rhel} <= 7)
BuildRequires:  vala-tools
%endif
BuildRequires:  wxGTK3-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gettext
BuildRequires:  gnustep-base-devel
BuildRequires:  %{_bindir}/gnustep-config
BuildRequires:  git-core
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
%if ! 0%{?rhel} || 0%{?rhel} > 7
BuildRequires:  python3-gobject-base
%endif
BuildRequires:  gtk-doc
BuildRequires:  itstool
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python%{python3_pkgversion}-Cython
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  llvm-devel
Requires:       ninja-build

%description
Meson is a build system designed to optimize programmer
productivity. It aims to do this by providing simple, out-of-the-box
support for modern software development tools and practices, such as
unit tests, coverage reports, Valgrind, CCache and the like.

%prep
%autosetup -p1
find -type f -name '*.py' -executable -exec sed -i -e '1s|.*|#!%{__python3}|' {} ';'

%build
%py3_build

%install
%py3_install
install -Dpm0644 data/macros.%{name} %{buildroot}%{rpmmacrodir}/macros.%{name}

%check
export MESON_PRINT_TEST_OUTPUT=1
%{__python3} ./run_tests.py %{?rhel:|| :}

%files
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}conf
%{_bindir}/%{name}introspect
%{_bindir}/%{name}test
%{_bindir}/wraptool
%{python3_sitelib}/%{libname}/
%{python3_sitelib}/%{name}-*.egg-info/
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}conf.1*
%{_mandir}/man1/%{name}introspect.1*
%{_mandir}/man1/%{name}test.1*
%{_mandir}/man1/wraptool.1*
%{rpmmacrodir}/macros.%{name}

%changelog
* Tue Aug 08 2017 Davide Cavalca <dcavalca@fb.com> - 0.41.2-2.fb1
- Facebook rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.41.2-1
- Update to 0.41.2

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 0.41.1-3
- Backport various gtk-doc fixes from upstream

* Thu Jul 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.41.1-2
- Strip trailing slash from pkg-config files

* Thu Jun 22 2017 Davide Cavalca <dcavalca@fb.com> 0.41.1-1.fb1
- Facebook rebuild

* Mon Jun 19 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.41.1-1
- Update to 0.41.1

* Wed Jun 14 2017 Davide Cavalca <dcavalca@fb.com> - 0.40.1-2.fb1
- build against python34 for CentOS 7
- make sure rpmmacrodir is defined

* Tue Jun 13 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.41.0-1
- Update to 0.41.0

* Wed May 31 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.40.1-2
- Don't run ldc tests

* Fri Apr 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.40.1-1
- Update to 0.40.1

* Sun Apr 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.40.0-1
- Update to 0.40.0

* Thu Apr 13 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.39.1-2
- Exclude ldc for module builds

* Thu Mar 16 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.39.1-1
- Update to 0.39.1

* Mon Mar 06 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.39.0-1
- Update to 0.39.0

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.38.1-1
- Update to 0.38.1

* Sun Jan 29 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.38.0-1
- Update to 0.38.0

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.37.1-2
- Rebuild for Python 3.6

* Tue Dec 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.37.1-1
- Update to 0.37.1

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.37.0-2
- Rebuild for Python 3.6

* Sun Dec 18 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.37.0-1
- Update to 0.37.0

* Thu Dec 15 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-4
- Backport more RPM macro fixes (FPC ticket #655)

* Tue Dec 13 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-3
- Backport fixes to RPM macros

* Sat Dec 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-2
- Print test output during build

* Mon Nov 14 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-1
- Update to 0.36.0

* Tue Oct 18 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.1-1
- Update to 0.35.1 (RHBZ #1385986)

* Tue Oct 11 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.0-3
- Backport couple of fixes

* Wed Oct 05 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.0-2
- Apply patch to fix FTBFS

* Mon Oct 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.0-1
- Update to 0.35.0

* Wed Sep 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.34.0-2
- Run D test suite

* Wed Sep 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.34.0-1
- Update to 0.34.0

* Tue Aug 09 2016 Jon Ciesla <limburgher@gmail.com> - 0.33.0-2
- Obsoletes fix.

* Tue Aug 09 2016 Jon Ciesla <limburgher@gmail.com> - 0.33.0-1
- 0.33.0
- GUI dropped upstream.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.31.0-1
- Update to 0.31.0

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.30.0-1
- Update to 0.30.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.29.0-1
- Update to 0.29.0

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.28.0-2
- Rebuilt for Boost 1.60

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.28.0-1
- 0.28.0

* Wed Nov 25 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.27.0-1
- 0.27.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 30 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.26.0-2
- Fix rpm macros for using optflags

* Sun Sep 13 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.26.0-1
- 0.26.0

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.25.0-4
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.25.0-2
- rebuild for Boost 1.58

* Sun Jul 12 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.25.0-1
- 0.25.0

* Sat Jul 11 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.0-3
- Update URLs
- drop unneded hacks in install section
- enable print test output for tests

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.0-1
- Update to 0.24.0

* Thu May 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-3.20150328git0ba1d54
- Update to latest git

* Thu May 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-3
- Add patch to accept .S files

* Wed Apr 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-2
- Add python3 to Requires (Thanks to Ilya Kyznetsov)

* Tue Mar 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-1
- 0.23.0

* Sat Mar 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-9.20150328git3b49b71
- Update to latest git

* Mon Mar 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-9.20150325git18550fe
- Update to latest git
- Include mesonintrospect

* Mon Mar 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-9.20150322git78d31ca
- Fix filelists for mesongui (python-bytecode-without-source)

* Sun Mar 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-8.20150322git78d31ca
- Enable C# tests

* Sun Mar 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150322git78d31ca
- update to latest git
- fix tests on arm

* Sat Mar 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150321gita084a8e
- update to latest git

* Mon Mar 16 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150316gitfa2c659
- update to latest git

* Tue Mar 10 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150310gitf9f51b1
- today's git snapshot with support for cool GNOME features
- re-enable wxGTK3 tests, package fixed in rawhide

* Thu Feb 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-6.git7581895
- split gui to subpkg
- update to latest snapshot
- enable tests

* Thu Feb 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-5.gitc6dbf98
- Fix packaging style
- Make package noarch

* Mon Feb 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-4.git.c6dbf98
- Use development version

* Sat Feb 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-3
- Add ninja-build to requires

* Thu Jan 22 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.0-2
- fix shebang in python files

* Wed Jan 21 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.0-1
- Initial package
