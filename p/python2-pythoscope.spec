%define modname pythoscope

Summary:    Unit Test Generator for Python
Name:       python2-%{modname}
Version:    0.4.3
Release:    3.1
Source0:    %{modname}-%{version}.tar.bz2
License:    MIT
Group:      Development/Libraries/Python
BuildArch:  noarch
URL:        https://pythoscope.org
BuildRequires:  python2-devel python2-setuptools

%description
Pythoscope is a unit test generator for programs written in Python.
It means it can produce a test suite that captures current behavior
of your application (so called characterization tests).
If you have a system written in Python and value testing,
Pythoscope can help you achieve a high test coverage.

%prep
%setup -q -n %{modname}-%{version}

%build
python2 setup.py build

%install
python2 setup.py install \
--prefix=%{_prefix} \
--root=$RPM_BUILD_ROOT

sed -i 's|/usr/bin/python$|/usr/bin/python2|' %{buildroot}%{_bindir}/*

%files
%doc README Changelog doc/*
%{_bindir}/*
%{python2_sitelib}/*

%changelog
* Wed Sep 25 2013 Wei-Lun Chao <bluebat@member.fsf.org> - 0.4.3
- Rebuilt for Fedora
* Sun Feb 28 2010 toms@suse.de
- First initial release 0.4.3
