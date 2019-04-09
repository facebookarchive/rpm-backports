%global srcname dcrpm

%ifos darwin
%global _arch noarch
%global _bindir /opt/homebrew/bin
%global python_sitelib /opt/homebrew/lib/python2.7/site-packages
%global dist .darwin
%endif

Name:           %{srcname}
Version:        0.4.0
Release:        1.fb1
Summary:        A tool to detect and correct common issues around RPM database corruption.

License:        GPL-2.0
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/facebookincubator/dcrpm/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        dcrpm.py

# Facebook-specific logging stuff
%if 0%{?facebook}
Source2:        logging.json
Source3:        scuba_logger.py
Suggests:       fb-everstore-clowder

%endif

BuildArch:      noarch

%ifos darwin
Requires:       py27-psutil
%else
BuildRequires:  python2-devel python-setuptools python2-pypandoc
BuildRequires:  python2-psutil python2-typing python2-mock

Requires:       python-setuptools python2-psutil
%endif

%description
A tool to detect and correct common issues around RPM database corruption.

%prep
%setup -n %{srcname}-%{version}

%build
%if 0%{?facebook}
cp %{SOURCE3} dcrpm/
%endif
%ifos linux
%py2_build
%endif

%install
%ifos darwin
mkdir -p %{buildroot}/%{python_sitelib}
cp -PR dcrpm %{buildroot}/%{python_sitelib}
mkdir -p %{buildroot}/%{_bindir}
install -m0755 %{SOURCE1} %{buildroot}/%{_bindir}/dcrpm
%else
%py2_install
%endif

%if 0%{?facebook}
mkdir -p %{buildroot}/%{_sysconfdir}
install -m0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/dcrpm-logging.json
%endif

%check
%ifos linux
%{__python2} setup.py test
%endif

%files
%ifos linux
%license LICENSE
%doc README.md HISTORY.md MANUAL_RPM_CLEANUP.md CONTRIBUTING.md CODE_OF_CONDUCT.md
%endif
%{python_sitelib}/*
%attr(0755, root, root) %{_bindir}/dcrpm
%if 0%{?facebook}
%{_sysconfdir}/dcrpm-logging.json
%endif

%changelog
* Wed Feb 20 2019 Igor Kanyuka <ikanyuka@fb.com> - 0.4.0-1.fb1
- Fix __db.001 holder detection

* Mon Jan 14 2019 Nikita Koshikov <nikitakoshikov@fb.com> - 0.3.1-1.fb1
- Fix rpm build via yummy

* Fri Jan 11 2019 Nikita Koshikov <nikitakoshikov@fb.com> - 0.3.0-1.fb1
- Release with Fedora support

* Wed Sep 19 2018 Davide Cavalca <dcavalca@fb.com> - 0.2.0-1.fb2
- Set Requires to ensure dependencies are always pulled in

* Thu Sep 17 2018 Davide Cavalca <dcavalca@fb.com> - 0.2.0-1.fb1
- Initial version
