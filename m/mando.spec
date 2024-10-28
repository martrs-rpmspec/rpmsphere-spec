%undefine _debugsource_packages

Name:           mando
Version:        1.8.2
Release:        19.1
Summary:        Interactive Camera-Projector System
Source0:        https://vision.eng.shu.ac.uk/jan/%{name}_%{version}.orig.tar.gz
Source1:        %name.videodev.h
URL:            https://mando.sourceforge.net/
Group:          User Interface/X Hardware Support
License:        GPLv2+
BuildRequires:  libpng-devel
BuildRequires:  gcc-c++ cmake
BuildRequires:  qt4-devel boost-devel f2c fftw3-devel
BuildRequires:  libdc1394-devel lapack-devel freeglut-devel
BuildRequires:  libXtst-devel blas-devel

%description
The software makes use of a low cost off-the shelf webcam that is calibrated
against a standard projector screen. The webcam is used to determine the
position of physical pointer (e.g. a pen) which is then used to virtually move
the X11 pointer. Point-and-click functionality has also been implemented.

%prep
%setup -q -c
cp %{SOURCE1} src/videodev.h
sed -i 's|<linux/videodev.h>|"videodev.h"|' src/image_v4linput.h
#FIXME
sed -i 's|retVal \* (Real)( 1.0 / retVal.num_elements() )|retVal|' src/fourier.tcc

%build
%cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_CXX_FLAGS="-std=gnu++14 -fPIE"
sed -i 's|-isystem /usr/include ||' *-linux-build/src/CMakeFiles/mando.dir/flags.make
%cmake_build

%install
rm -rf $RPM_BUILD_ROOT
#cd build
%cmake_install
mv %{buildroot}%{_datadir}/icons/%{name}.png %{buildroot}%{_datadir}/pixmaps

%files
%doc AUTHORS README COPYING TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}*

%changelog
* Wed Apr 11 2012 Wei-Lun Chao <bluebat@member.fsf.org> - 1.8.2
- Rebuilt for Fedora
* Thu Dec 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6-1mdv2009.1
+ Revision: 313195
- lowercase ImageMagick
* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 1.6-1mdv2009.0
+ Revision: 218422
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix no-buildroot-tag
* Fri Feb 08 2008 Funda Wang <fundawang@mandriva.org> 1.6-1mdv2008.1
+ Revision: 164190
- br mesaglut-devel
- BR libxtst-devel
- import mando
