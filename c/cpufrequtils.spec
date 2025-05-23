%define libname libcpufreq

Name: cpufrequtils
Version: 008
Release: 3
Summary: Tools to determine and set CPUfreq settings
License: GPLv2
Group: System/Base
URL: https://www.kernel.org/pub/linux/utils/kernel/cpufreq/cpufrequtils.html
Source: https://www.kernel.org/pub/linux/utils/kernel/cpufreq/cpufrequtils-%version.tar.bz2
Patch0: 0001-Only-x86-has-cpuid-instruction.patch
Patch1: 0001-Only-x86-has-cpuid-h.patch
Requires: %libname = %version-%release

%description
To make access to the Linux kernel cpufreq subsystem easier for users
and cpufreq userspace tools, the cpufrequtils package was created. It
contains a library used by other programs (libcpufreq), command line
tools to determine current CPUfreq settings and to modify them
(cpufreq-info and cpufreq-set), and debug tools.

%package -n %libname
Summary: Library for %name
License: GPLv2
Group: Development/C

%description -n %libname
This packages contains some library needed by %name.

%package -n %libname-devel
Summary: Headers for developing programs that will use %libname
License: GPLv2
Group: Development/C
Requires: %libname = %version-%release
Obsoletes: %name-devel
Provides: %name-devel

%description -n %libname-devel
This package contains the headers that programmers will need to develop
applications which will use %libname.

%prep
%setup -q
%patch 0 -p1
%patch 1 -p1
sed -i 's/--mode=/--tag=CC --mode=/' Makefile

%build
%make_build CFLAGS="%optflags" V=true

%install
%make_install mandir=%_mandir libdir=%_libdir V=true
%find_lang cpufrequtils

%files -f cpufrequtils.lang
%_bindir/*
%_mandir/man1/*

%files -n %libname
%_libdir/libcpufreq.so.*

%files -n %libname-devel
%_includedir/*
%_libdir/libcpufreq.so

%changelog
* Sun Sep 12 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 008
- Rebuilt for Fedora
* Sun Apr 19 2020 Michael Shigorin <mike@altlinux.org> 008-alt3
- further fixed build on non-x86 architectures, notably E2K
- minor spec cleanup
* Thu Feb 14 2019 Gleb F-Malinovskiy <glebfm@altlinux.org> 008-alt2
- Fixed build on non-x86 architectures (patch by Zhang Le).
* Tue Jul 24 2012 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 008-alt1.1
- Rebuilt for set-versions
* Thu Aug 05 2010 Victor Forsiuk <force@altlinux.org> 008-alt1
- Version 008.
* Mon Jun 15 2009 Victor Forsyuk <force@altlinux.org> 005-alt3
- Fix FTBFS (specify a tag for libtool).
* Fri Dec 12 2008 Victor Forsyuk <force@altlinux.org> 005-alt2
- Remove obsolete ldconfig calls.
* Mon Aug 11 2008 Victor Forsyuk <force@altlinux.org> 005-alt1
- Version 005.
* Wed Jul 30 2008 Victor Forsyuk <force@altlinux.org> 004-alt1
- Version 004 (new: removed dependency on libsysfs, added support
  for cpufreq statistics).
* Mon May 26 2008 Victor Forsyuk <force@altlinux.org> 003-alt1
- Version 003.
* Thu Apr 19 2007 Victor Forsyuk <force@altlinux.org> 002-alt2
- Fix 64 bit build.
* Wed Apr 18 2007 Victor Forsyuk <force@altlinux.org> 002-alt1
- Version 002.
- Eliminate duplication of library in utils package.
* Tue Mar 28 2006 Anton Farygin <rider@altlinux.ru> 001-alt1
- new version
* Mon Mar 20 2006 Anton Farygin <rider@altlinux.ru> 0.4-alt3
- fixed build
* Tue Feb 21 2006 Anton Farygin <rider@altlinux.ru> 0.4-alt2
- split package to library and utils part
* Wed Feb 01 2006 Anton Farygin <rider@altlinux.ru> 0.4-alt1
- new version
* Wed Jun 29 2005 Anton Farygin <rider@altlinux.ru> 0.3-alt1
- first build for ALT Linux
