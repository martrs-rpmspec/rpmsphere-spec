Summary: Gtk interface to make annotations on the screen
Name: ardesia
Version: 1.1
Release: 1
License: GPLv3
Source0: https://ardesia.googlecode.com/files/%{name}-%{version}.tar.gz
Source1: %{name}-0.8.zh_TW.po
Group: Applications/Desktop
URL: https://code.google.com/p/ardesia/
BuildRequires: intltool
BuildRequires: gtk2-devel, atk-devel, cairo-devel, fontconfig-devel, pango-devel, gsl-devel, libxml2-devel
BuildRequires: libgsf-devel
Requires: recordmydesktop

%description
Ardesia help you to make colored free-hand annotations with digital ink
on your computer screen, record it and share on the network.

You can use the tool to make effective on-screen presentation, highlight
things or point out things of interest. The tool facilitates the online
presentations and demos showing in real time your computer screen to anyone
in the network. Create nice tutorial and documentation saving the desktop
images with your free hand annotations. You can draw lines with different
strength, select color, erase things and draw arrows. You can free-hand draw
geometrical shapes using the shape recognizer, insert text with the keyboard
and highlight screen areas. You can draw upon the desktop or select an image
as background.

Ardesia works with all the pointing device; you can use a mouse, a graphic tablet,
a touch screen, a cheap professional wiimote whiteboard or a commercial whiteboard.

%prep
%setup -q
#sed -i 's/2\.24\.0/2.22.0/' configure*
#sed -i '529,534d' desktop/Makefile.in
echo 'zh_TW' >> po/LINGUAS
cp %{SOURCE1} po/zh_TW.po

%build
LDFLAGS=-Wl,--allow-multiple-definition
%configure
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_datadir}/doc/%{name}
%find_lang %{name}

%files -f %{name}.lang
%doc README INSTALL AUTHORS ChangeLog TODO COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.1*

%changelog
* Sun Oct 16 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 1.1
- Rebuilt for Fedora
