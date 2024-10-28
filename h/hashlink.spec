%global __os_install_post %{nil}
%undefine _debugsource_packages
%define _unpackaged_files_terminate_build 1

Name: hashlink
Version: 1.12
Release: 1
Summary: HashLink is a virtual machine for Haxe
License: MIT
Group: Development/Other
URL: https://hashlink.haxe.org/
Source: %name-%version.tar.gz
BuildRequires: cmake libGLU-devel SDL2-devel libdb-devel libpng-devel openssl-devel libjpeg-devel libuv-devel libvorbis-devel zlib-devel
BuildRequires: mbedtls-devel openal-soft-devel libuv-devel sqlite-devel

%package devel
Summary: %summary
Group: %group

%description
%summary

%description devel
%summary

%prep
%setup -q
#sed -i '4i #define HL_CONSOLE' libs/fmt/fmt.c
sed -i -e 's|-lturbojpeg|-ljpeg|' -e 's|/lib|/%{_lib}|' Makefile

%build
%cmake -D BUILD_TESTING=OFF .
%ifarch aarch64
sed -i -e 's|-msse2||' -e 's|-mfpmath=sse||' -e 's|-m$(MARCH)||' Makefile
%endif
%make_build PREFIX=/usr

%install
%make_install PREFIX=%{buildroot}/usr
install -m644 src/hlc_main.c %buildroot%_includedir/hlc_main.c
mv %{buildroot}%{_libdir}/libhl.so %{buildroot}%{_libdir}/libhl.so.%{version}.0
ln -s libhl.so.%{version}.0 %{buildroot}%{_libdir}/libhl.so.1
ln -s libhl.so.%{version}.0 %{buildroot}%{_libdir}/libhl.so

%files
%doc LICENSE README.md
#%doc AUTHORS ChangeLog NEWS README THANKS TODO contrib/ manual/
%_bindir/hl
%_libdir/libhl.so.*
%_libdir/*.hdll

%files devel
%_libdir/libhl.so
%_includedir/hl.h
%_includedir/hlc.h
%_includedir/hlc_main.c

%changelog
* Sun Mar 26 2023 Wei-Lun Chao <bluebat@member.fsf.org> - 1.12
- Rebuilt for Fedora
* Mon May 18 2020 Denis Smirnov <mithraen@altlinux.ru> 1.11-alt2
- add /usr/include/hlc_main.c for HL/C support
* Mon May 18 2020 Denis Smirnov <mithraen@altlinux.ru> 1.11-alt1
- first build for Sisyphus
