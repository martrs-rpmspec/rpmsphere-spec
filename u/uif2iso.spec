Name:           uif2iso
Version:        0.1.4
Release:        7.1
License:        GPL
BuildRequires:  cmake zlib-devel openssl-devel
Group:          System/Utilities
Summary:        Tool for converting the UIF files to ISO
Source0:        uif2iso.c
Source1:        %name.CMakeLists.txt

%description
Tool for converting the UIF files (Universal Image Format, used by MagicISO) to ISO.

%prep
cp %{SOURCE0} .
cp %{SOURCE1} CMakeLists.txt
cat /etc/fstab

%build
cmake -DCMAKE_INSTALL_PREFIX=/usr .
%make_build

%install
%make_install

%files
%{_bindir}/%{name}

%changelog
* Sun Sep 09 2012 Wei-Lun Chao <bluebat@member.fsf.org> - 0.1.4
- Rebuilt for Fedora
* Mon Sep  7 2009 crrodriguez@suse.de
- fix build
* Tue Dec 25 2007 crrodriguez@suse.de
- initial version
