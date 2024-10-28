%undefine _debugsource_packages

Name: rox-filer
Version: 2.11
Release: 1
Summary: ROX desktop enviroment
License: GNU GPL
Group: Graphical desktop/Other
URL: https://rox.sourceforge.net/
Source: https://prdownloads.sourceforge.net/%{name}/%{name}-%version.tar.bz2
Source1: rox-startup.sh
Source2: rox-filer.desktop
Patch0: rox-i18n-standard-path.patch
Patch1: rox-images-standard-path.patch
Patch2: rox-user-config.patch
Patch3: rox-fix-help-path.patch
Patch50: rox-2.3-rootmenu.patch
Patch51: rox-2.3-workplace.patch
BuildRequires: fontconfig imake libXt-devel gtk2-devel libxml2-devel imake pkgconfig 

%description
ROX is a desktop environment, like GNOME, KDE and XFCE.
It is an attempt to bring some of the good features from RISC OS to Unix and Linux.

%prep
%setup -q
#%patch 0 -p1
sed -i 's|"%s/Messages", app_dir|"/usr/share/locale"|' ROX-Filer/src/i18n.c
%patch 1 -p1
#%%patch 2 -p1
%patch 3 -p1
#%%patch 50 -p1
#%%patch 51 -p1

%build
export LDFLAGS=-Wl,--allow-multiple-definition
%__mkdir ROX-Filer/build
cd ROX-Filer/build
../src/configure --enable-rox 
sed -i 's|-lX11|-lX11 -lm -ldl|' Makefile
make
cd ../src/po
./dist

%install
%__mkdir -p %buildroot%_libdir/rox/ROX-Filer
%__mkdir -p %buildroot/usr/{bin,share/{mime/packages,Choices,man/man1,rox/{images,help,ROX/MIME}}}
%__install -m 755 ROX-Filer/ROX-Filer %buildroot%_libdir/rox/ROX-Filer
%__install -m 755 ROX-Filer/AppRun %buildroot%_libdir/rox/ROX-Filer
%__install -m 644 rox.xml %buildroot%_datadir/mime/packages
%__install -m 644 rox.1 %buildroot%_mandir/man1
%__install -m 755 Choices/MIME-types/application_postscript %buildroot%_datadir/Choices
%__install -m 755 Choices/MIME-types/text %buildroot%_datadir/Choices
%__install -m 755 Choices/MIME-types/text_html %buildroot%_datadir/Choices
#install languages
%__install -Dm 644 ROX-Filer/Messages/cs/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/cs/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/da/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/da/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/de/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/de/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/es/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/es/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/fi/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/fi/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/fr/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/fr/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/hu/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/hu/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/it/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/it/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/ja/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/ja/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/nl/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/nl/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/no/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/no/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/pl/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/pl/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/pt_BR/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/pt_BR/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/ro/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/ro/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/ru/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/ru/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/sv/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/sv/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/zh_CN/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/zh_CN/LC_MESSAGES/ROX-Filer.mo
%__install -Dm 644 ROX-Filer/Messages/zh_TW/LC_MESSAGES/ROX-Filer.mo %buildroot%_datadir/locale/zh_TW/LC_MESSAGES/ROX-Filer.mo

#install default theme
%__install -m 644 ROX-Filer/ROX/index.theme %buildroot%_datadir/rox/ROX
%__cp ROX-Filer/ROX/MIME/* %buildroot%_datadir/rox/ROX/MIME/
%__cp ROX-Filer/images/* %buildroot%_datadir/rox/images/

%__cp ROX-Filer/Help/*.html %buildroot%_datadir/rox/help
%__install -m 644 ROX-Filer/.DirIcon %buildroot%_libdir/rox/ROX-Filer
%__install -m 644 ROX-Filer/AppInfo.xml %buildroot%_libdir/rox/ROX-Filer
%__install -m 644 ROX-Filer/Options.xml %buildroot%_libdir/rox/ROX-Filer
%__install -m 644 ROX-Filer/style.css %buildroot%_libdir/rox/ROX-Filer
%__install -m 755 %SOURCE1 %buildroot%_bindir/rox
%__install -Dm 644 %SOURCE2 %buildroot%_datadir/applications/%{name}.desktop
%__sed -i "s|@LIBDIR@|%_libdir|g" %buildroot%_bindir/rox

%files
%doc ROX-Filer/Help/{COPYING,Changes,README,README-es,TODO}
%_bindir/*
%_libdir/rox/*
%_datadir/rox/*
%_datadir/mime/packages/*
%_datadir/Choices
%_datadir/locale/*/LC_MESSAGES/ROX-Filer.mo
%_datadir/applications/%{name}.desktop
%_mandir/man1/*

%changelog
* Tue Mar 20 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 2.11
- Rebuilt for Fedora
* Thu Oct 05 2006 Eugene Ostapets <eostapets@altlinux.ru> 2.5-alt1
- new version
* Fri Aug 12 2005 Eugene Ostapets <eostapets@altlinux.ru> 2.3-alt1
- new version
* Wed Aug 10 2005 Eugene Ostapets <eostapets@altlinux.ru> 2.2.0-alt1
- initial build 
