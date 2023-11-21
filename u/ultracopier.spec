%undefine _debugsource_packages

Name:		ultracopier
Version:	2.2.4.7
Release:	1
License:	GPLv3+
Group:		File tools
URL:		https://ultracopier.first-world.info/
Source:		https://files.first-world.info/ultracopier/%{version}/ultracopier-src-%{version}.tar.xz
BuildRequires:	qt5-qtbase-devel
Summary:	The QT advanced copier
Obsoletes:	supercopier

%description
Ultracopier is an advanced file copier with copy list management.

%prep
%setup -q -n %{name}-src
sed -i '11i #include <cstdint>' lib/qt-tar-xz/QTarDecode.h cpp11addition.h
sed -i '9i #include <cstring>' cpp11addition.cpp

%build
qmake-qt5
lrelease-qt5 `find . -name *.ts`
%make_build

%install
rm -rf %{buildroot}
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 resources/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm644 resources/%{name}-16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -Dm644 resources/%{name}-128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
sed -i -e 's/^Icon=%{name}.png$/Icon=%{name}/g' %{buildroot}%{_datadir}/applications/*

%clean
%__rm -rf %{buildroot}

%files
%doc COPYING README.*
%{_bindir}/ultracopier
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sun Apr 11 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 2.2.4.7
- Rebuilt for Fedora
* Fri Feb 17 2017 Andrey Bondrov <andrey.bondrov@rosalab.ru> 0.2.0.16-5
- (7263b13) MassBuild#1257: Increase release tag
