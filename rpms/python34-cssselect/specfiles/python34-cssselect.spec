# %global with_tests 1

Name:           python34-cssselect
Version:        0.9.1
Release:        10.fb2
Group:          Development/Libraries
Summary:        Parses CSS3 Selectors and translates them to XPath 1.0

License:        BSD
URL:            http://packages.python.org/cssselect/
Source0:        https://pypi.python.org/packages/source/c/cssselect/cssselect-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python34-devel python34-setuptools
%if 0%{?with_tests}
BuildRequires:  python34-lxml
%endif # if with_tests

%description
Cssselect parses CSS3 Selectors and translates them to XPath 1.0 expressions.
Such expressions can be used in lxml or another XPath engine to find the
matching elements in an XML or HTML document.

%prep
%setup -q -n cssselect-%{version}

%build
%{__python3} setup.py build

%check
%if 0%{?with_tests}
PYTHONPATH=$(pwd) %{__python3} cssselect/tests.py
%endif # with_tests

%install
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT/%{python3_sitelib}/cssselect/tests.py

%files
%doc AUTHORS docs README.rst CHANGES LICENSE PKG-INFO
%{python3_sitelib}/cssselect*

%changelog
* Thu Jul 28 2016 Davide Cavalca <dcavalca@fb.com> - 0.9.1-10.fb2
- enable back tests now that python34-lxml is in the repo

* Wed Jul 27 2016 Davide Cavalca <dcavalca@fb.com> - 0.9.1-10.fb1
- Facebook rebuild
- Rename to python34-cssselect and make it build on CentOS 7
- Temporarily disable tests as python34-lxml is not available yet

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-10
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.9.1-8
- Enable tests

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.9.1-7
- Rebuilt for Python3.5 rebuild
- Disable tests as (circular dependency with python-lxml)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 14 2014 Ralph Bean <rbean@redhat.com> - 0.9.1-5
- Modernize with_python3 conditional.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.1-3
- Enable tests again.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Bootstrap test running (circular dependency with python-lxml)

* Fri Jan 17 2014 Eduardo Echeverria <echevemaster@gmail.com> 0.9.1-1
- Update to latest upstream.
- although this package have py3 support, the resultant python3 package
  doesn't existed, reason? On install section, py3 setup install must be first,
  if not, with every running of setup.py install, setup.py overwrite the files,
  this behaviour has been fixed
- Workaround for python2 macro in epel versions
- use python2 macro instead of python

* Thu Jul 25 2013 Eric Smith <brouhaha@fedoraproject.org> 0.8-1
- Update to latest upstream.
- Added Python 3 support.
- Added EL6 support (uses Python 2.6 rather than 2.7).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Kevin Fenzi <kevin@scrye.com> 0.7.1-3
- Add tests.

* Fri Nov 09 2012 Kevin Fenzi <kevin@scrye.com> 0.7.1-2
- Fixes from review.

* Fri Nov 09 2012 Kevin Fenzi <kevin@scrye.com> 0.7.1-1
- Initial version for review
