Name: caph
Version: 1.1
Release: 5.1
Group: Games/Puzzles
Summary: A sandbox game, based on physics
Source: %name-%version.tar.bz2
Patch0: caph-1.1-alt-verbose.patch
Patch1: caph-1.1-alt-debuginfo.patch
URL: https://caphgame.sourceforge.net/
License: GPLv3
BuildRequires: mesa-libGL-devel SDL-devel libpng-devel

%description
It is a sandbox game, based on physics. The game aim is to make contact
red object with green object. You can use various objects, solid, wire
(rope), and bendable objects. Gravitation will help you.

%prep
%setup -q
%patch 0 -p2
%patch 1 -p2
sed -i '
/^#define SYS_DATA_DIR/c\
#define SYS_DATA_DIR "%_gamesdatadir/%name/"
' src/caph.c

cat > %name.sh <<@@@
#!/bin/sh

CAPHDIR="\$HOME/.%name"
SHAREDIR="%_gamesdatadir/%name"
test -d "\$CAPHDIR" && cd "\$CAPHDIR" || {
rm -rf "\$CAPHDIR"
mkdir -p "\$CAPHDIR"
cd "\$CAPHDIR"
cp \`find "\$SHAREDIR"/* -maxdepth 0 -type f\` .
for D in \`find "\$SHAREDIR"/* -maxdepth 0 -type d\`; do
  LD=\`basename \$D\`
  mkdir -p "\$LD"
  ln -s "\$D"/* "\$LD"/
done
}

exec "\$0.bin"
@@@

#mkdir bin

# TODO desktop

%build
cd src
./confg
./build

%install
mkdir -p "%buildroot%_datadir"
cp -r share/caph "%buildroot%_datadir/%name"
install -D bin/%name %buildroot%_bindir/%name.bin
install -m755 -D %name.sh %buildroot%_bindir/%name

%files
%doc doc/*
%_bindir/*
%_datadir/%name

%changelog
* Tue Apr 19 2016 Wei-Lun Chao <bluebat@member.fsf.org> - 1.1
- Rebuilt for Fedora
* Thu Oct 04 2012 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.1-alt1.1
- Rebuilt with libpng15
* Fri Dec 24 2010 Fr. Br. George <george@altlinux.ru> 1.1-alt1
- Autobuild version bump to 1.1
* Mon Oct 04 2010 Fr. Br. George <george@altlinux.ru> 1.0-alt1
- Initial build from scratch
