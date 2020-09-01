%global srcname flunk_dependent_remove
Name:    python3-dnf-flunk-dependent-remove
Version: 1.0
Release: 1.fb1%{?dist}
Summary: Do not remove packages recursively via automation
License: GPL-2.0
BuildArch: noarch
Source0: %{srcname}.py
BuildRequires: python3-devel
Requires: dnf

%description
Do not allow "dnf -y remove" to expand the list of packages to remove to
include packages which require one of the explicitly listed packages.
Fail the request instead.

%install
# contrary to the name, this runs with the RPM is BUILT, not when it's
# installed on a server.
install -D -m0644 %{SOURCE0} \
  %{buildroot}/%{python3_sitelib}/dnf-plugins/%{srcname}.py

%files
%defattr(-, root, root)
%{python3_sitelib}/dnf-plugins/%{srcname}.py
%{python3_sitelib}/dnf-plugins/__pycache__/*

%changelog
* Fri Jun 12 2020 William Herrin <wherrin@fb.com> - 1.0-1.fb1
- initial version

