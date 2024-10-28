Summary: identd daemon with masquerading support
Name: pimpd
Version: 0.8
Release: 7.1
License: GPL
Group: System/Daemons
Source: pimpd-%{version}.tar.gz
Source1: auth.tar.gz
Patch0: fakeident.diff

%description
ident daemon with support for linux masquerading firewalls.

%prep
%setup -a 1
%patch 0 -p1
sed -i 's|-Wall|-Wall -fPIE|' Makefile

%build
make -j 2

%install
%{__rm} -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/usr/sbin
mkdir -p ${RPM_BUILD_ROOT}/etc/xinetd.d
install pimpd ${RPM_BUILD_ROOT}/usr/sbin
install auth  ${RPM_BUILD_ROOT}/etc/xinetd.d

%files
%doc README
/usr/sbin/pimpd
/etc/xinetd.d/auth

%changelog
* Tue Aug 21 2012 Wei-Lun Chao <bluebat@member.fsf.org> - 0.8
- Rebuilt for Fedora
* Thu Jun 26 2008 admin@eregion.de
- bogus changelog
