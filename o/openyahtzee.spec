Name: openyahtzee
Version: 1.9
Release: 1
Summary: A full-featured version of the classic dice game Yahtzee
Group: Games/Boards
URL: https://openyahtzee.sourceforge.net
License: GPL
Source: https://downloads.sourceforge.net/openyahtzee/%{name}-%{version}.tar.bz2
BuildRequires: wxGTK-devel

%description
Open Yahtzee is an open-source (free) version
of the classic dice game Yahtzee.

%prep
%setup -q
sed -i '1i #include<unistd.h>' src/DBwrapper.cpp

%build
%configure
sed -i 's/-pthread/-pthread -fpermissive -ldl/' src/Makefile
make

%install
rm -rf %{buildroot}
%makeinstall

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%files
%{_bindir}/openyahtzee
%{_datadir}/applications/openyahtzee.desktop
%{_datadir}/pixmaps/openyahtzee.png

%changelog
* Tue Mar 20 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 1.9
- Rebuilt for Fedora
* Sun Aug 01 2010 Texstar <texstar at gmail.com> 1.9-1pclos2010
- create package
