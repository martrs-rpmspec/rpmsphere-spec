%ifarch %ix86 x86_64
  %bcond_without gold
%else
  %bcond_with gold
%endif

# Documentation install path
%if 0%{?fedora} < 20
  %global llvmdocdir() %{_docdir}/%1-%{version}
%else
  %global llvmdocdir() %{_docdir}/%1
%endif

%global major_version 3.4

Name:           llvm34
Version:        %{major_version}.2
Release:        10
Summary:        The Low Level Virtual Machine

Group:          Development/Languages
License:        NCSA
URL:            https://llvm.org/

# source archives
Source0:        https://llvm.org/releases/%{version}/llvm-%{version}.src.tar.gz

# multilib fixes
Source10:       llvm-Config-config.h
Source11:       llvm-Config-llvm-config.h

# patches
Patch11:        0001-data-install-preserve-timestamps.patch
Patch12:        0002-linker-flags-speedup-memory.patch

# temporary measure to get ppc64le building, if perhaps not working
Patch21:        0001-PPC64LE-ELFv2-ABI-updates-for-the-.opd-section.patch

BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  groff
BuildRequires:  libffi-devel
BuildRequires:  libtool-ltdl-devel
%if %{with gold}
BuildRequires:  binutils-devel
%endif
BuildRequires:  ncurses-devel
BuildRequires:  zip
# for DejaGNU test suite
BuildRequires:  dejagnu tcl-devel python2-devel
# pod2man moved to perl-podlators in F19
BuildRequires:  %{_bindir}/pod2man
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
LLVM is a compiler infrastructure designed for compile-time,
link-time, runtime, and idle-time optimization of programs from
arbitrary programming languages.  The compiler infrastructure includes
mirror sets of programming tools as well as libraries with equivalent
functionality.


%package devel
Summary:        Libraries and header files for LLVM
Group:          Development/Languages
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libffi-devel
Requires:       libstdc++-devel >= 3.4
Requires:       ncurses-devel
Requires(posttrans): /usr/sbin/alternatives
Requires(postun):    /usr/sbin/alternatives

%description devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.


%package doc
Summary:        Documentation for LLVM
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.


%package libs
Summary:        LLVM shared libraries
Group:          System Environment/Libraries

%description libs
Shared libraries for the LLVM compiler infrastructure.


%package static
Summary:        LLVM static libraries
Group:          Development/Languages
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libraries for the LLVM compiler infrastructure.  Not recommended
for general consumption.


%prep
%setup -q -n llvm-%{version}.src
rm -rf tools/clang tools/lldb projects/compiler-rt

%patch 11 -p1
%patch 12 -p1
%patch 21 -p1

# fix library paths
sed -i.orig 's|/lib /usr/lib $lt_ld_extra|%{_libdir} $lt_ld_extra|' configure
sed -i.orig -e 's|(PROJ_prefix)/lib|(PROJ_prefix)/%{_lib}/%{name}|g' \
            -e 's|(PROJ_prefix)/include|(PROJ_prefix)/include/%{name}|g' \
            Makefile.config.in
sed -i.orig -e 's|/lib\>|/%{_lib}/%{name}|g' \
            -e 's|/include\>|/include/%{name}|g' \
            tools/llvm-config/llvm-config.cpp

%build
# clang is lovely and all, but fedora builds with gcc
export CC=gcc
export CXX=c++
%configure \
  --libdir=%{_libdir}/%{name} \
  --includedir=%{_includedir}/%{name} \
  --disable-polly \
  --disable-libcpp \
  --enable-cxx11 \
  --enable-clang-arcmt \
  --enable-clang-static-analyzer \
  --enable-clang-rewriter \
  --enable-optimized \
  --disable-profiling \
  --disable-assertions \
  --disable-werror \
  --disable-expensive-checks \
  --enable-debug-runtime \
  --enable-keep-symbols \
  --enable-jit \
  --enable-docs \
  --disable-doxygen \
  --enable-threads \
  --enable-pthreads \
  --enable-zlib \
  --enable-pic \
  --enable-shared \
  --disable-embed-stdcxx \
  --enable-timestamps \
  --enable-backtraces \
  --enable-targets=x86,powerpc,arm,aarch64,cpp,nvptx,systemz \
  --enable-experimental-targets=R600 \
  --enable-bindings=none \
  --enable-libffi \
  --enable-ltdl-install \
  \
%ifarch armv7hl armv7l
  --with-cpu=cortex-a8 \
  --with-tune=cortex-a8 \
  --with-arch=armv7-a \
  --with-float=hard \
  --with-fpu=vfpv3-d16 \
  --with-abi=aapcs-linux \
%endif
  \
%if %{with gold}
  --with-binutils-include=%{_includedir} \
%endif
  --with-c-include-dirs=%{_includedir}:$(ls -d1 %{_prefix}/lib/gcc/%{_target_cpu}*/*/include | tr "\\n" ":")

sed -i 's|-Wno-format|-Wno-format-security|' lib/Target/CppBackend/Makefile

make %{_smp_mflags} REQUIRES_RTTI=1 VERBOSE=1 \
%ifarch ppc
  OPTIMIZE_OPTION="%{optflags} -UPPC"
%else
  OPTIMIZE_OPTION="%{optflags}"
%endif


%install
make install DESTDIR=%{buildroot} PROJ_docsdir=/moredocs

# multilib fixes
mv %{buildroot}%{_bindir}/llvm-config{,-%{__isa_bits}}

pushd %{buildroot}%{_includedir}/%{name}/llvm/Config
mv config.h config-%{__isa_bits}.h
cp -p %{SOURCE10} config.h
mv llvm-config.h llvm-config-%{__isa_bits}.h
cp -p %{SOURCE11} llvm-config.h
popd

# Create ld.so.conf.d entry
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf << EOF
%{_libdir}/%{name}
EOF

# Get rid of erroneously installed example files.
rm %{buildroot}%{_libdir}/%{name}/*LLVMHello.*
strip %{buildroot}%{_libdir}/%{name}/*.so

# remove executable bit from static libraries
find %{buildroot}%{_libdir} -name "*.a" -type f -print0 | xargs -0 chmod -x

# Install documentation documentation
find %{buildroot}/moredocs/ -name "*.tar.gz" -print0 | xargs -0 rm -rf
mkdir -p %{buildroot}%{_docdir}

# llvm-doc
mkdir -p %{buildroot}%{llvmdocdir %{name}-doc}
cp -ar examples %{buildroot}%{llvmdocdir %{name}-doc}/examples
find %{buildroot}%{llvmdocdir %{name}-doc} -name Makefile -o -name CMakeLists.txt -o -name LLVMBuild.txt -print0 | xargs -0 rm -f

# suffix bindir files with major version to avoid conflict with llvm
for i in %{buildroot}%{_bindir}/*; do
    mv $i $i-%{major_version}
done
ln -sf llvm-ar-%{major_version} %{buildroot}%{_bindir}/llvm-ranlib-%{major_version}

# delete the rest of installed documentation (because it's bad)
rm -rf %{buildroot}/moredocs

# install CMake modules
mkdir -p %{buildroot}%{_datadir}/%{name}/cmake/
cp -p cmake/modules/*.cmake %{buildroot}%{_datadir}/%{name}/cmake/

# remove RPATHs
file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
file %{buildroot}/%{_libdir}/%{name}/*.so | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d

%check
# the Koji build server does not seem to have enough RAM
# for the default 16 threads

# the || : is wrong, i know, but the git snaps fail to make check due to
# broken makefiles in the doc dirs.

# LLVM test suite failing on ARM, PPC64 and s390(x)
mkdir -p %{buildroot}%{llvmdocdir %{name}-devel}
make -k check LIT_ARGS="-v -j4" | tee %{buildroot}%{llvmdocdir %{name}-devel}/testlog-%{_arch}.txt || :


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%posttrans devel
# link llvm-config to the platform-specific file;
# use ISA bits as priority so that 64-bit is preferred
# over 32-bit if both are installed
#
# XXX ew alternatives though. seems like it'd be better to install a
# shell script that cases on $(arch) and calls out to the appropriate
# llvm-config-%d.
alternatives \
  --install \
  %{_bindir}/llvm-config \
  llvm-config \
  %{_bindir}/llvm-config-%{__isa_bits}-%{major_version} \
  %{__isa_bits}

%postun devel
if [ $1 -eq 0 ]; then
  alternatives --remove llvm-config \
    %{_bindir}/llvm-config-%{__isa_bits}-%{major_version}
fi
exit 0


%files
%doc CREDITS.TXT
%doc README.txt
%{_bindir}/bugpoint-%{major_version}
%{_bindir}/llc-%{major_version}
%{_bindir}/lli-%{major_version}
%{_bindir}/lli-child-target-%{major_version}
%exclude %{_bindir}/llvm-config-%{__isa_bits}-%{major_version}
%{_bindir}/llvm*-%{major_version}
%{_bindir}/macho-dump-%{major_version}
%{_bindir}/opt-%{major_version}

%files devel
%doc %{llvmdocdir %{name}-devel}/
%{_bindir}/llvm-config-%{__isa_bits}-%{major_version}
%{_includedir}/%{name}
%{_datadir}/%{name}

%files libs
%license LICENSE.TXT
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so

%files static
%{_libdir}/%{name}/*.a

%files doc
%doc %{llvmdocdir %{name}-doc}/

%changelog
* Thu Jul 04 2019 Wei-Lun Chao <bluebat@member.fsf.org> - 3.4.2
- Rebuilt for Fedora

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Jens Petersen <petersen@redhat.com> - 3.4.2-8
- Fix alternatives llvm-config to use the version suffix (Milan Bouchet-Valat)
- Fix include dir used by llvm-config to reflect the actual (suffixed) location
  of files. (Milan Bouchet-Valat)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.4.2-6
- Rebuilt for GCC 5 C++11 ABI change

* Thu Nov 13 2014 Jens Petersen <petersen@redhat.com> - 3.4.2-5
- fix handling of doc files

* Thu Nov 13 2014 Jens Petersen <petersen@redhat.com> - 3.4.2-4
- BR python2-devel instead of python (#1161014)
- drop -O3 config from llvm.spec for now (#1161014)
- use license tag for license file and move license to libs (#1161014)
- remove unused clang patches

* Wed Nov 12 2014 Jens Petersen <petersen@redhat.com> - 3.4.2-3
- rename datadir to llvm34 (#1161014)
- remove all conditioned out clang, lldb, crt, ocaml
- drop defattr's

* Fri Nov  7 2014 Jens Petersen <petersen@redhat.com> - 3.4.2-2
- suffix bindir files with major version
- move include dirs under llvm34

* Thu Nov  6 2014 Jens Petersen <petersen@redhat.com> - 3.4.2-1
- New llvm34 package: do not build clang
  - needed for armv7 ghc since current ghc releases do not support llvm-3.5
- llvm34-libs installable parallel to llvm-libs

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Adam Jackson <ajax@redhat.com> 3.4-15
- Restore ppc64le fix

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 3.4-14
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Thu Jul 24 2014 Adam Jackson <ajax@redhat.com> 3.4-13
- llvm and clang 3.4.2

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 3.4-12
- OCaml 4.02.0 beta rebuild.

* Wed Jun 11 2014 Adam Jackson <ajax@redhat.com> 3.4-11
- Different attempt to default to hard-float on arm (#803433)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Adam Jackson <ajax@redhat.com> 3.4-9
- Backport a ppc64le fix to get things started bootstrapping

* Mon Jun 02 2014 Adam Jackson <ajax@redhat.com> 3.4-8
- Attempt to default to hard-float on arm (#803433)

* Thu May 29 2014 Adam Jackson <ajax@redhat.com> 3.4-7
- Update to llvm 3.4.1 plus a few things from svn
- Drop radeonsi patch, merged in 3.4.1

* Thu Mar 27 2014 Rex Dieter <rdieter@fedoraproject.org> 3.4-6
- -libs: Obsoletes: OpenGTL libQtGTL

* Wed Mar 19 2014 Dave Airlie <airlied@redhat.com> 3.4-5
- backport patches from 3.5 to enable GL3.3 on radeonsi

* Fri Jan 31 2014 Kyle McMartin <kyle@redhat.com> 3.4-4
- Disable lldb on everything but x86_64, and i686. It hasn't been ported
  beyond those platforms so far.

* Fri Jan 17 2014 Dave Airlie <airlied@redhat.com> 3.4-3
- bump nvr for lldb on ppc disable

* Tue Jan 14 2014 Dave Airlie <airlied@redhat.com> 3.4-2
- add ncurses-devel BR and Requires

* Tue Jan 14 2014 Dave Airlie <airlied@redhat.com> 3.4-1
- update to llvm 3.4 release

* Fri Dec 20 2013 Jan Vcelak <jvcelak@fedoraproject.org> 3.3-4
- remove RPATHs
- run ldconfig when installing lldb (#1044431)
- fix: scan-build manual page is installed into wrong location (#1038829)
- fix: requirements for llvm-ocaml-devel packages (#975914)
- add LLVM cmake modules into llvm-devel (#914713)

* Sat Nov 30 2013 Jan Vcelak <jvcelak@fedoraproject.org> 3.3-3
- properly obsolete clang-doc subpackage (#1035268)
- clang-analyzer: fix scan-build search for compiler (#982645)
- clang-analyzer: switch package architecture to noarch

* Thu Nov 21 2013 Jan Vcelak <jvcelak@fedoraproject.org> 3.3-2
- fix build failure, missing __clear_cache() declaration

* Tue Nov 12 2013 Jan Vcelak <jvcelak@fedoraproject.org> 3.3-1
- upgrade to 3.3 release
- add compiler-rt, enables address sanitizer (#949489)
- add LLDB - debugger from LLVM project (#1009406)
- clean up documentation

* Thu Oct 17 2013 Jakub Jelinek <jakub@redhat.com> - 3.3-0.10.rc3
- Rebuild for gcc 4.8.2

* Sat Sep 14 2013 Petr Pisar <ppisar@redhat.com> - 3.3-0.9.rc3
- Rebuild for OCaml 4.01.0.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-0.8.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.3-0.7.rc3
- Perl 5.18 rebuild

* Mon Jun 10 2013 Adam Jackson <ajax@redhat.com> 3.3-0.6.rc3
- llvm 3.3-rc3

* Tue Jun 04 2013 Adam Jackson <ajax@redhat.com> 3.3-0.5.rc2
- Rebuild for gcc 4.8.1

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 3.3-0.4.rc2
- llvm 3.3-rc2

* Sat May 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.3-0.3.20130507
- Enable aarch64 target

* Tue May 07 2013 Adam Jackson <ajax@redhat.com> 3.3-0.1.20130507
- Bump to LLVM 3.3svn
- Enable s390 backend

* Mon May 06 2013 Adam Jackson <ajax@redhat.com> 3.2-6
- Only build codegen backends for arches that actually exist in Fedora

* Wed May 01 2013 Adam Jackson <ajax@redhat.com> 3.2-5
- Tweak ld flags for memory usage and performance

* Thu Apr  4 2013 Jens Petersen <petersen@redhat.com> - 3.2-4
- fix bogus date for 2.9-0.2.rc1
- drop insufficient llvm-3.2-clang-driver-secondary-arch-triplets.patch

* Sun Mar 31 2013 Dennis Gilmore <dennis@ausil.us> - 3.2-3
- add a hack to clang defaulting arm to hardfloat

* Fri Mar 08 2013 Adam Jackson <ajax@redhat.com> 3.2-2
- Update R600 patches
- Move static libs to -static subpackage
- Prep for F18 backport

* Wed Feb 13 2013 Jens Petersen <petersen@redhat.com> - 3.2-1
- update to 3.2
- update R600 patches to Tom Stellard's git tree
- llvm-fix-ghc.patch is upstream
- llvm-3.1-docs-pod-markup-fixes.patch no longer needed
- add llvm-3.2-clang-driver-secondary-arch-triplets.patch (#803433)
- build with gcc/g++ even if clang is installed
- llvm-config.1 manpage is no longer

* Mon Feb  4 2013 Jens Petersen <petersen@redhat.com> - 3.1-16
- bring back configuration for gcc arch include dir (Yury Zaytsev, #893817)
  which was dropped in 3.0-0.1.rc3
- BR gcc and gcc-c++ with gcc_version

* Thu Jan 31 2013 Jens Petersen <petersen@redhat.com> - 3.1-15
- move lvm-config manpage to devel subpackage (#855882)
- pod2man moved to perl-podlators in F19

* Fri Jan 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.1-14
- Rebuilt for GCC 4.8.0

* Wed Jan 23 2013 Jens Petersen <petersen@redhat.com> - 3.1-13
- fix some docs pod markup errors to build with new perl-Pod-Parser

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 3.1-12
- Rebuild for OCaml 4.00.1.

* Mon Sep 24 2012 Michel Salim <salimma@fedoraproject.org> - 3.1-11
- Actually build against GCC 4.7.2

* Mon Sep 24 2012 Michel Salim <salimma@fedoraproject.org> - 3.1-10
- Rebuild for GCC 4.7.2

* Tue Aug 14 2012 Dan Horák <dan[at]danny.cz> - 3.1-9
- Apply clang patches only when clang is being built

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.1-7
- Rename patch as it actually fixes Haskell

* Thu Jul 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.1-6
- Add patch to fix building OCAML on ARM

* Wed Jul  4 2012 Michel Salim <salimma@fedoraproject.org> - 3.1-5
- Actually set runtime dependency on libstdc++ 4.7.1

* Mon Jul  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.1-4
- Rebuild for new libstdc++ bump

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 3.1-3
- Rebuild for OCaml 4.00.0.

* Fri Jun  8 2012 Michel Salim <salimma@fedoraproject.org> - 3.1-2
- Rebuild for ocaml 4.00.0 beta

* Sun Jun 03 2012 Dave Airlie <airlied@redhat.com> 3.1-1
- rebase to 3.1 + add r600 patches from Tom Stellar

* Fri May 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0-13
- Add compiler build options for ARM hardfp

* Sun May  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.0-12
- Bump build

* Fri Mar 30 2012 Michel Alexandre Salim <michel@hermione.localdomain> - 3.0-11
- Replace overly-broad dependency on gcc-c++ with gcc and libstdc++-devel
- Pin clang's dependency on libstdc++-devel to the version used for building
- Standardize on bcond for conditional build options
- Remove /lib from search path, everything is now in /usr/lib*

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 3.0-10
- Build without -ftree-pre as a workaround for clang segfaulting
  on x86_64 (#791365)

* Sat Mar 17 2012 Karsten Hopp <karsten@redhat.com> 3.0-9
- undefine PPC on ppc as a temporary workaround for 
  https://llvm.org/bugs/show_bug.cgi?id=10969 and 
  RHBZ#769803

* Sat Feb 25 2012 Michel Salim <salimma@fedoraproject.org> - 3.0-8
- Apply upstream patch to properly link LLVMgold against LTO

* Fri Feb 24 2012 Michel Salim <salimma@fedoraproject.org> - 3.0-7
- Build LLVMgold plugin on supported architectures

* Tue Feb  7 2012 Michel Salim <salimma@fedoraproject.org> - 3.0-6
- Make subpackage dependencies arch-specific
- Make LLVM test failures non-fatal on ARM architectures as well (# 770208)
- Save LLVM test log on platforms where it fails

* Sun Feb  5 2012 Michel Salim <salimma@fedoraproject.org> - 3.0-5
- Clang test suite yields unexpected failures with GCC 4.7.0. Make
  this non-fatal and save the results
- Multilib fix for harcoded ld search path in ./configure script

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 3.0-4
- Rebuild for OCaml 3.12.1.

* Wed Dec 14 2011 Adam Jackson <ajax@redhat.com> 3.0-3
- Also ExcludeArch: ppc* in RHEL

* Tue Dec 13 2011 Adam Jackson <ajax@redhat.com> 3.0-2
- ExcludeArch: s390* in RHEL since the native backend has disappeared in 3.0

* Sun Dec 11 2011 Michel Salim <salimma@fedoraproject.org> - 3.0-1
- Update to final 3.0 release

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 3.0-0.2.rc3
- RHEL customization: disable clang, --enable-targets=host

* Fri Nov 11 2011 Michel Salim <salimma@fedoraproject.org> - 3.0-0.1.rc3
- Update to 3.0rc3

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 2.9-5
- don't fail the build on failing tests on ppc(64) and s390(x)

* Fri Sep 30 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-4
- Apply upstream patch for Operator.h C++0x incompatibility (# 737365)

* Sat Aug  6 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-3
- Disable LLVM test suite on ppc64 architecture  (# 728604)
- Disable clang test suite on ppc* architectures (-)

* Wed Aug  3 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-2
- Add runtime dependency of -devel on libffi-devel

* Mon Aug  1 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-1
- Update to 2.9
- Depend on libffi to allow the LLVM interpreter to call external functions
- Build with RTTI enabled, needed by e.g. Rubinius (# 722714)
- Fix multilib installation (# 699416)
- Fix incorrect platform-specific include path on i686

* Tue May 31 2011 Karsten Hopp <karsten@redhat.com> 2.9-0.4.rc2
- enable ppc64 build

* Fri Mar 25 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-0.3.rc2
- Update to 2.9rc2

* Thu Mar 17 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-0.2.rc1
- Split shared libraries into separate subpackage
- Don't include test logs; breaks multilib (# 666195)
- clang++: also search for platform-specific include files (# 680644)

* Thu Mar 10 2011 Michel Salim <salimma@fedoraproject.org> - 2.9-0.1.rc1
- Update to 2.9rc1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Richard W.M. Jones <rjones@redhat.com> - 2.8-6
- Rebuild for OCaml 3.12 (https://fedoraproject.org/wiki/Features/OCaml3.12).

* Sat Nov 27 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-5
- clang now requires gcc-c++ for linking and headers (bug #654560)

* Fri Nov 12 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-4
- Backport support for C++0x (# 648990)

* Fri Oct 15 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-3
- Re-add omitted %%{_includedir}

* Thu Oct 14 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-2
- Add correct C include directory at compile time (# 641500)

* Tue Oct 12 2010 Michel Salim <salimma@fedoraproject.org> - 2.8-1
- Update to 2.8 release

* Wed Sep 29 2010 jkeating - 2.7-10
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-9
- Dynamically determine C++ include path at compile time (# 630474)
- Remove unneeded BuildRoot field and clean section

* Wed Sep 15 2010 Dennis Gilmore <dennis@ausil.us> - 2.7-8
- disable ocaml support on sparc64

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.7-7
- recompiling .py files against Python 2.7 (rhbz#623332)

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 2.7-6
- conditionalize ocaml support

* Mon Jun  7 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-5
- Make the new noarch -doc obsoletes older (arched) subpackages

* Sat Jun  5 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-4
- Add F-12/x86_64 and F-13 C++ header paths

* Wed May 26 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-3
- Revert to disabling apidoc by default

* Mon May 24 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-2
- Exclude llm-gcc manpages
- Turn on apidoc generation
- Build with srcdir=objdir, otherwise clang doxygen build fails

* Sun May  2 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-1
- Update to final 2.7 release

* Sun Mar 28 2010 Michel Salim <salimma@fedoraproject.org> - 2.7-0.1.pre1
- Update to first 2.7 pre-release

* Fri Sep 18 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.6.pre2
- Update to 2.6 pre-release2
- -devel subpackage now virtually provides -static

* Wed Sep  9 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.5.pre1
- Disable var tracking assignments on PPC

* Wed Sep  9 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.4.pre1
- Don't adjust clang include dir; files there are noarch (bz#521893)
- Enable clang unit tests
- clang and clang-analyzer renamed; no longer depend on llvm at runtime

* Mon Sep  7 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.3.pre1
- Package Clang's static analyzer tools

* Mon Sep  7 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.2.pre1
- PIC is now enabled by default; explicitly disable on %%{ix86}

* Mon Sep  7 2009 Michel Salim <salimma@fedoraproject.org> - 2.6-0.1.pre1
- First 2.6 prerelease
- Enable Clang front-end
- Enable debuginfo generation

* Sat Sep  5 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-6
- Disable assertions (needed by OpenGTL, bz#521261)
- Align spec file with upstream build instructions
- Enable unit tests

* Sat Aug 22 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-5
- Only disable PIC on %%ix86; ppc actually needs it

* Sat Aug 22 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-4
- Disable use of position-independent code on 32-bit platforms
  (buggy in LLVM <= 2.5)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar  4 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-2
- Remove build scripts; they require the build directory to work

* Wed Mar  4 2009 Michel Salim <salimma@fedoraproject.org> - 2.5-1
- Update to 2.5
- Package build scripts (bug #457881)

* Tue Dec  2 2008 Michel Salim <salimma@fedoraproject.org> - 2.4-2
- Patched build process for the OCaml binding

* Tue Dec  2 2008 Michel Salim <salimma@fedoraproject.org> - 2.4-1
- Update to 2.4
- Package Ocaml binding

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.3-2
- Add dependency on groff

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.3-1
- LLVM 2.3

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2-4
- fix license tags

* Wed Mar  5 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.2-3
- Fix compilation problems with gcc 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.1-2
- Fix review comments

* Sun Jan 20 2008 Bryan O'Sullivan <bos@serpentine.com> - 2.1-1
- Initial version
