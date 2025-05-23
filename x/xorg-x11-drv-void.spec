Name: xorg-x11-drv-void
Version: 1.4.1
Release: 5.1
Epoch: 1
Summary: Null input driver
License: MIT/X11
Group: System/X11
URL: https://xorg.freedesktop.org
BuildRequires: xorg-x11-server-devel
Source: xorg-drv-void-%version.tar
Patch0: xorg-drv-void-%version-alt2.patch

%description
void is an dummy/null Xorg input driver.  It doesn't connect
to any physical device, and it never delivers any events.  It functions
as  both  a  pointer and keyboard device, and may be used as X server's
core pointer and/or core keyboard.  It's purpose  is  to  allow  the  X
server to operate without a core pointer and/or core keyboard.

%prep
%setup -q -n xorg-drv-void-%version
%patch 0 -p1
cp -f /usr/bin/libtool .

%build
autoreconf -ifv
%configure \
        --with-xorg-module-dir=%{_libdir}/xorg/modules \
        --disable-static

%make_build

%install
%make_install

%files
%{_libdir}/xorg/modules/input/*.so
%exclude %{_libdir}/xorg/modules/input/*.la
%{_mandir}/man4/*

%changelog
* Thu Jul 26 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 1.4.1
- Rebuilt for Fedora
* Thu Dec 01 2016 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.1-alt2
- requires XORG_ABI_XINPUT = 24.1
* Fri Nov 27 2015 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.1-alt1
- 1.4.1
* Fri Oct 10 2014 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.0-alt6
- requires XORG_ABI_XINPUT = 21.0
* Fri Jan 31 2014 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.0-alt5
- requires XORG_ABI_XINPUT = 15.0
* Wed Mar 06 2013 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.0-alt4
- requires XORG_ABI_XINPUT = 14.1
* Fri Jan 18 2013 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.0-alt3
- requires XORG_ABI_XINPUT = 13.1
* Sun Mar 25 2012 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.0-alt2
- requires XORG_ABI_XINPUT = 12.0
* Tue Aug 30 2011 Valery Inozemtsev <shrek@altlinux.ru> 1:1.4.0-alt1
- 1.4.0
* Wed Dec 08 2010 Valery Inozemtsev <shrek@altlinux.ru> 1:1.3.1-alt1
- 1.3.1
* Sun Aug 22 2010 Valery Inozemtsev <shrek@altlinux.ru> 1:1.3.0-alt2
- requires XORG_ABI_XINPUT = 11.0
* Thu Oct 08 2009 Valery Inozemtsev <shrek@altlinux.ru> 1:1.3.0-alt1
- 1.3.0
* Fri Feb 27 2009 Valery Inozemtsev <shrek@altlinux.ru> 1:1.2.0-alt2
- requires XORG_ABI_XINPUT = 4.0
* Wed Feb 25 2009 Valery Inozemtsev <shrek@altlinux.ru> 1:1.2.0-alt1
- 1.2.0
* Wed Aug 27 2008 Valery Inozemtsev <shrek@altlinux.ru> 1:1.1.1-alt3
- requires XORG_ABI_XINPUT = 2.1
* Wed Jun 04 2008 Valery Inozemtsev <shrek@altlinux.ru> 1:1.1.1-alt2
- renamed xorg-x11-drv-void to xorg-drv-void
- added requires XORG_ABI_XINPUT = 2.0
* Mon Sep 10 2007 Valery Inozemtsev <shrek@altlinux.ru> 1:1.1.1-alt1
- 1.1.1
* Sat May 13 2006 Valery Inozemtsev <shrek@altlinux.ru> 1:1.1.0-alt1
- 1.1.0
* Wed Dec 28 2005 Valery Inozemtsev <shrek@altlinux.ru> 1:1.0.0.5-alt1
- Xorg-7.0
* Sun Dec 04 2005 Valery Inozemtsev <shrek@altlinux.ru> 1.0.0.3-alt1
- Xorg-7.0RC3
* Sun Nov 27 2005 Valery Inozemtsev <shrek@altlinux.ru> 1.0.0.2-alt0.1
- initial release
