%undefine _debugsource_packages

Name: corners
Version: 1.4.3
Release: 1
License: GPLv.2
Summary: A logical board game as known as Halma
Summary (ru_RU.KOI8-R): Игра в уголки (другое название -- хальма)
Group: Games/Boards
Source: %name-%version.tar.bz2
Source1: %name.desktop
Patch0: corners-1.4.3-alt-gcc4.7.patch
BuildRequires: gcc-c++ gtk2-devel

%description
Corners is a logical board game as known as Halma. This game has two AI's; one
of them isn't too hard to play with, whereas the second one is relatively
strong and you need to have good mathematical abilities to defeat it.

%description -l ru_RU.KOI8-R
В игре участвуют два игрока, фишки которых расположены в противоположных
углах доски. Цель игры - переместить все свои фишки из одного угла доски в
противоположный. Каждый ход игрок либо передвигает одну из своих фишек в
соседнюю клетку, либо перепрыгивает ею через одну или несколько своих или
чужих фишек, при этом передвижения осуществляются по горизонтали и
вертикали. Выигрывает тот игрок, который переместит все свои фишки в
противоположный угол за меньшее число ходов.

%prep
%setup -q
%patch 0 -p1
sed -i -e '36i extern "C++" {' -e '98i }' lcore_src/funcs.h
sed -i -e '6i extern "C++" {' -e '$i }' lcore_src/pointers.h
sed -i -e '7i extern "C++" {' -e '49i }' lcore_src/strings.h

%build
make

%install
mkdir -p %buildroot%_bindir
%makeinstall INSTALL_DIR=%buildroot%_prefix
mv %buildroot%_datadir/%name/%name %buildroot%_bindir/%name.bin
cat > %buildroot%_bindir/%name <<EOF
#!/bin/sh
cd %_datadir/%name
%_bindir/%name.bin
EOF
install -D %{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README
%{_datadir}/%{name}
%{_bindir}/%{name}*
%{_datadir}/pixmaps/%name.png
%{_datadir}/applications/%name.desktop

%changelog
* Sun May 05 2013 Wei-Lun Chao <bluebat@member.fsf.org> - 1.4.3
- Rebuilt for Fedora
* Tue Nov 20 2012 Br. George <george@altlinux.ru> 1.4.3-alt1
- Autobuild version bump to 1.4.3
- Patching makefile
* Tue Nov 13 2012 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.4-alt1.1
- Fixed build with gcc 4.7
* Wed Jul 27 2011 Fr. Br. George <george@altlinux.ru> 1.4-alt1
- Autobuild version bump to 1.4
* Fri Apr 17 2009 Fr. Br. George <george@altlinux.ru> 1.2-alt2
- Desktop file added
* Fri Apr 17 2009 Fr. Br. George <george@altlinux.ru> 1.2-alt1
- Initial build from scratch
