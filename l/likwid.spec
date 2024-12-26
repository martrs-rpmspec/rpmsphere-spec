%undefine _debugsource_packages
%global __spec_install_post %{nil}

Name:               likwid
Version:            5.3.0
Release:            1
Summary:            High Performance Multi-Threading Support Tools
Source0:            https://likwid.googlecode.com/files/likwid-%{version}.tar.gz
Patch1:             likwid-lib.patch
Patch2:             likwid-optflags.patch
URL:                https://code.google.com/p/likwid/
Group:              System/Base
License:            GNU General Public License version 2 or later (GPL v2 or later)
BuildRequires:      gcc make glibc-devel

%description
Likwid is a set of easy to use command line tools for Linux. It works with any
standard Linux kernel. Likwid is lightweight and adds no overhead during measurements.

It supports programmers in developing high performance multi-threaded programs.
"Likwid" stands for "Like I knew what I am doing". It contains the following
tools: likwid-topology, which shows thread and cache topology; likwid-perfCtr,
which measures hardware performance counters on Intel and AMD processors;
likwid-features, which shows and toggles hardware prefetch control bits on
Intel Core 2 processors; likwid-pin, which pins a threaded application without
touching its code (it supports pthreads, Intel OpenMP, and gcc OpenMP).

%package devel
Summary:            High Performance Multi-Threading Support Tools
Group:              Development/Libraries/C and C++

%description devel
Likwid is a set of easy to use command line tools for Linux.

It supports programmers in developing high performance multi-threaded programs.
"Likwid" stands for "Like I knew what I am doing". It contains the following
tools: likwid-topology, which shows thread and cache topology; likwid-perfCtr,
which measures hardware performance counters on Intel and AMD processors;
likwid-features, which shows and toggles hardware prefetch control bits on
Intel Core 2 processors; likwid-pin, which pins a threaded application without
touching its code (it supports pthreads, Intel OpenMP, and gcc OpenMP).

It works with any standard Linux kernel.
Likwid is lightweight and adds no overhead during measurements.

%prep
%setup -q
#patch 1
#patch 2

%build
%__make \
    CC="%__cc" \
    OPTFLAGS="%{optflags}" \
    COMPILER="GCC" \
    PREFIX="%{_prefix}" \
    MANPREFIX="%{_mandir}" \
    LIBLIKWIDPIN="%{_libdir}/%{name}/liblikwidpin.so" \
    V=1 Q=""

%install
%__rm -rf "$RPM_BUILD_ROOT"
%__make %{?jobs:-j%{jobs}} \
    CC="%__cc" \
    OPTFLAGS="%{optflags}" \
    COMPILER="GCC" \
    PREFIX="$RPM_BUILD_ROOT%{_prefix}" \
    MANPREFIX="$RPM_BUILD_ROOT%{_mandir}" \
    LIBLIKWIDPIN="%{_libdir}/%{name}/liblikwidpin.so" \
    LIB="%{_libdir}" \
    V=1 Q="" \
    install

#__install -d "$RPM_BUILD_ROOT%{_libdir}/%{name}"
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}

# for backwards compatibility with < 2.0:
#__ln_s likwid-perfctr "$RPM_BUILD_ROOT%{_bindir}/likwid-perfCtr"

%files
%doc COPYING README.* CHANGELOG
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/%{name}
%{_datadir}/lua/%{name}.lua
%{_libdir}/lib*.so.* 
%{_mandir}/man1/*

%files devel
%{_includedir}/*.h
%{_libdir}/lib*.so

%changelog
* Sun Dec 8 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 5.3.0
- Rebuilt for Fedora
* Sat Jan 15 2011 pascal.bleser@opensuse.org
- moved preload library liblikwidpin.so to %%{_libdir}/likwid/
- update to 2.2:
  * a hotfix for a build problem with direct MSR mode
  * millisecond resolution for likwid-perfctr daemon mode
  * improved error recovery for the MSR daemon
- changed from 2.1:
  * performance groups were improved in likwid-perfctr (NUMA group for AMD K10)
  * the new likwid-mpirun script was added, which is an mpirun wrapper to enable pinning for MPI and MPI/OpenMP hybrid applications
  * likwid-perfctr supports output in files with placeholders for MPI parallel applications
  * thread domain M (Memory) was added for NUMA domains
  * pin functionality was integrated for likwid-perfctr
  * likwid-msrD was added, which is an msr daemon to enable secure access to msr registers in security sensitive environments
  * many bug fixes and small improvements were made
* Tue Oct 12 2010 pascal.bleser@opensuse.org
- update to 2.0:
  * full support for AMD Magny Cours was added
  * the core events of Intel Nehalem EX are now supported
  * likwid-pin can also use logical pinning now
  * a daemon mode was added for likwid-perfctr, supporting very lightweight monitoring -- this daemon can also be used to generate timeline graphs for a specific application
- changes from 2.0beta:
  * the likwid-bench application was added, allowing rapid multithreaded prototyping of low level benchmarks
  * logical pinning on the node/socket level was added in likwid-pin
  * NUMA topology support was added in likwid-topology
  * likwid-pin can set NUMA mempolicy to interleave
  * event sets for likwid-perfCtr are configurable and extensible with simple text files
  * extensive help for group configurations is available from the command line
  * a flag for silent execution in likwid-pin was added
  * statistical output (Sum, Max, Min, Avg) is produced for threaded measurements in likwid-perfCtr
  * execution was made faster for likwid-topology and all print switches
* Mon Jul 26 2010 pascal.bleser@opensuse.org
- update to 1.1:
  * fixes a bug that occurred if you were using likwid-perfCtr with OpenMP using the marker API and pinning the threads with likwid-pin
* Tue Jul 13 2010 pascal.bleser@opensuse.org
- initial package (1.0)
