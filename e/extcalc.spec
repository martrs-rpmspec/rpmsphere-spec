Summary:        A multifunctional scientific graphic calculator
Name:           extcalc
Version:        0.9.3
Release:        25.1
License:        GPL-2.0+
Group:          Applications/Engineering
URL:            https://sourceforge.net/projects/extcalc-linux/
Source0:        https://sourceforge.net/projects/extcalc-linux/files/extcalc-linux/%{version}/extcalc-%{version}-1.tar.gz
BuildRequires: gcc-c++, cmake, qt4-devel, mesa-libGL-devel

%description
Extcalc is a multifunctional scientific graphic calculator for Linux with
features like graph drawing, graph analysis and calculation of scientific
functions. Extcalc also provides an integrated programming language.

%prep
%setup -q -n %{name}-%{version}-1
sed -i -e 's|/usr/local|/usr|' -e 's|${QT_LIBRARIES}|${QT_LIBRARIES} -lGL|' CMakeLists.txt

%build
%cmake .
sed -i -e 's|-O3||' -e 's|-Werror=format-security||' */CMakeCache.txt */CMakeFiles/extcalc.dir/link.txt */CMakeFiles/extcalc.dir/flags.make
%cmake_build
                                                                                
%install
rm -rf $RPM_BUILD_ROOT
%cmake_install
mv $RPM_BUILD_ROOT%{_datadir}/icons $RPM_BUILD_ROOT%{_datadir}/pixmaps

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}*

%changelog
* Sun Oct 21 2012 Wei-Lun Chao <bluebat@member.fsf.org> - 0.9.3
- Rebuilt for Fedora
* Tue Sep  4 2012 anixx@opensuse.org
- initial release
