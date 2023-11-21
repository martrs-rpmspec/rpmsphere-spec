%global srcname openastro.org-data

Name:           openastro-data
Version:        1.9
Release:        4
Summary:        Astrology data
License:        GPLv3+
URL:            https://www.openastro.org
Source0:        https://www.openastro.org/download.php?file=source&type=data#/%{srcname}_%{version}.orig.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%description
Data for the open source astrology program.

%prep
%autosetup -n %{srcname}-%{version}
sed -i '18i py_modules=[],' setup.py

%build
%py3_build

%install
%py3_install

%files
%license COPYING
%{python3_sitelib}/*
%{_datadir}/openastro.org
%{_datadir}/swisseph

%changelog
* Mon Sep 28 2020 Wei-Lun Chao <bluebat@member.fsf.org> - 1.9
- Rebuilt for Fedora
* Thu Feb 11 2016 Jens Petersen <petersen@redhat.com>
- Initial package
