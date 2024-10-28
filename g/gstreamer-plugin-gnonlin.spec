%define oname gnonlin

Name: gstreamer-plugin-gnonlin
Version: 0.10.16
Release: 2.1
Summary: GStreamer extension library for non-linear editing
Group: Video
License: LGPL
URL: https://gstreamer.freedesktop.org/
Source0: %oname-%version.tar
Source1: common.tar
Patch0: %oname-%version.patch
#BuildRequires: gnome-libs-devel
BuildRequires: gtk-doc w3m
BuildRequires: gstreamer-plugins-base-devel
#BuildRequires: python-encodings

%description
Gnonlin is a library built on top of GStreamer (https://gstreamer.net)
which provides support for writing non-linear audio and video editing
applications. It introduces the concept of a timeline.

%prep
%setup -q -n %oname-%version -a1
%patch 0 -p1

%build
autoreconf -vfi
%configure \
        --with-default-audiosrc=pulsesrc \
        --with-default-audiosink=pulsesink \
        --with-default-videosrc=v4l2src \
        --with-default-videosink=xvimagesink \
        --disable-static
%make_build

%install
%make_install

%files
%doc AUTHORS NEWS README RELEASE
%exclude %{_libdir}/gstreamer-0.10/libgnl.la
%{_libdir}/gstreamer-0.10/libgnl.so

%changelog
* Thu Jun 14 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 0.10.16
- Rebuilt for Fedora
* Wed Apr 17 2013 Dmitry V. Levin (QA) <qa_ldv@altlinux.org> 0.10.16-alt1.qa1
- NMU: rebuilt for debuginfo.
* Tue Sep 07 2010 Valery Inozemtsev <shrek@altlinux.ru> 0.10.16-alt1
- 0.10.16
* Tue Mar 09 2010 Valery Inozemtsev <shrek@altlinux.ru> 0.10.15-alt1
- 0.10.15
* Thu Feb 11 2010 Valery Inozemtsev <shrek@altlinux.ru> 0.10.14-alt1
- 0.10.14
* Mon Sep 07 2009 Valery Inozemtsev <shrek@altlinux.ru> 0.10.13-alt1
- 0.10.13
* Fri Sep 04 2009 Valery Inozemtsev <shrek@altlinux.ru> 0.10.12.3-alt1
- 0.10.12.3
* Sun Aug 30 2009 Valery Inozemtsev <shrek@altlinux.ru> 0.10.12.2-alt1
- 0.10.12.2
* Tue Aug 11 2009 Valery Inozemtsev <shrek@altlinux.ru> 0.10.12-alt1
- 0.10.12
* Sun May 24 2009 Valery Inozemtsev <shrek@altlinux.ru> 0.10.11-alt1
- 0.10.11
* Sun Apr 26 2009 Valery Inozemtsev <shrek@altlinux.ru> 0.10.10-alt1
- 0.10.10
* Sun May 18 2008 Igor Zubkov <icesik@altlinux.org> 0.10.9-alt2
- rebuild
* Wed Aug 08 2007 Igor Zubkov <icesik@altlinux.org> 0.10.9-alt1
- 0.10.8 -> 0.10.9
* Sat May 05 2007 Igor Zubkov <icesik@altlinux.org> 0.10.8-alt1
- 0.10.7 -> 0.10.8
* Fri May 04 2007 Igor Zubkov <icesik@altlinux.org> 0.10.7-alt1
- 0.10.6 -> 0.10.7
- remove obsolete patch
- spec clean up
- update Url
* Thu Apr 12 2007 Vitaly Lipatov <lav@altlinux.ru> 0.10.6-alt1
- new version 0.10.6
- fix packager
- disable static libs (fix bug #11456)
* Sun Sep 10 2006 Vitaly Lipatov <lav@altlinux.ru> 0.10.5-alt0.1
- new version (0.10.5)
* Mon May 08 2006 Vitaly Lipatov <lav@altlinux.ru> 0.10.3-alt0.1
- new version (0.10.3)
- fix source URL
- remove -devel package
* Sun Apr 30 2006 Vitaly Lipatov <lav@altlinux.ru> 0.10.0.5-alt0.1
- new version (0.10.0.5)
- add patch against as-needed
* Sat Dec 31 2005 Vitaly Lipatov <lav@altlinux.ru> 0.10.0.3-alt0.1
- initial build for ALT Linux Sisyphus
* Thu Jul 14 2005 Edward Hervey <edward at fluendo dot com>
- Removed gnonlin-config*
* Mon Jun 27 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- cleanup of spec
* Mon Mar 21 2005 Edward Hervey <bilboed at bilboed dot com>
- First version of spec
