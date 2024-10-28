%undefine _debugsource_packages

Name:           gelemental
Summary:        Periodic Table Viewer
Version:        2.0.1
Release:        1
License:        GPL, MIT
URL:            https://github.com/ginggs/gelemental
Group:          Productivity/Scientific/Chemistry
Vendor:         openSUSE-Education
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Patch1:         gelemental-1.2.0-gcc43.patch
BuildRequires:  libpng-devel
BuildRequires:  glibmm24-devel >= 2.6
BuildRequires:  gtkmm24-devel >= 2.6
Requires:       glibmm24 >= 2.6
Requires:       gtkmm24 >= 2.6
BuildRequires:  desktop-file-utils
BuildRequires:  gettext-devel
BuildRequires:  gcc-c++
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig
BuildRequires:  automake

%description
gElemental is a GTK+ periodic table viewer with detailed information on 
the chemical elements. It uses the GTK+ toolkit and is available for Linux 
and other GTK+/GNOME platforms.

Authors:
--------
    Kevin Daughtridge

%package devel
Summary:        Development files for gElemetal
Requires:       %name = %version
BuildRequires:  glibmm24-devel
Requires:       pango-devel
Group:          Development/Librares/Other

%description devel
Files needed for doing gElemental development.

Authors:
--------
    Kevin Daughtridge

%prep
%setup -q
#patch1 -p1
#sed -i 's|glib/gmem\.h|glib.h|' libelemental/misc/extras.cc
#sed -i 's|glib/gmessages\.h|glib.h|' libelemental/misc/widgets.cc
#sed -i 's|glib/g.*\.h|glib.h|' src/main.cc
#sed -i '250s|false|NULL|' src/dialogs.cc
sed -i '29i #include <pango/pango-markup.h>' libelemental/value.cc

%build
export CXXFLAGS="-std=c++11 -fPIC"
%configure --disable-static
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
install -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_datadir}/applications/gelemental.desktop
rm $RPM_BUILD_ROOT%{_libdir}/libelemental.la
%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS COPYING COPYING.DATA NEWS README TODO TRANSLATORS
%doc %{_mandir}/man1/gelemental.1* 
%{_bindir}/gelemental
%{_libdir}/libelemental.so*
%exclude %{_libdir}/libelemental.so
%{_datadir}/applications/gelemental.desktop
%{_datadir}/icons/hicolor/*

%files devel
%{_includedir}/libelemental
%{_libdir}/libelemental.so
%{_libdir}/pkgconfig/libelemental.pc

%changelog
* Sun Sep 25 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 2.0.1
- Rebuilt for Fedora
* Sun Jun 29 2008 kirill.kirillov@gmail.com
- gelemental-1.2.0-gcc43.patch (added "#include <limits>" to value.hh)
* Tue Mar 18 2008 lars@linux-schulserver.de
- disable static
- move libelemental.so and libelemental.pc to -devel
- run /sbin/ldconfig
- devel package should require glibmm2-devel and pango-devel
- use %%suse_update_desktop_file macro
- add a GenericName to the desktop file
* Mon Oct  1 2007 kirill.kirillov@gmail.com
- Update to version 1.2.0
* Fri Jul 13 2007 kirill.kirillov@gmail.com
- Initial build of 1.0.0
