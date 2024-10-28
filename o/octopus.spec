%undefine _debugsource_packages

Name:           octopus
Summary:        A TDDFT code
Version:        12.0
Release:        1
License:        GPLv2+
Group:          Applications/Engineering
Source:         https://www.tddft.org/programs/octopus/download/%{name}-%{version}.tar.gz
URL:            https://octopus-code.org/wiki/Main_Page
BuildRequires:  blas-devel
BuildRequires:  fftw-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc-gfortran
BuildRequires:  gd-devel
BuildRequires:  gsl-devel
BuildRequires:  lapack-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libX11-devel
BuildRequires:  libXpm-devel
BuildRequires:  netcdf-devel
BuildRequires:  perl-interpreter
BuildRequires:  zlib-devel
BuildRequires:  libxc-devel
BuildRequires:  mpich-devel
BuildRequires:  environment-modules
#BuildRequires: openmpi-devel

%description
Octopus is a scientific program aimed at the ab initio virtual 
experimentation on a hopefully ever increasing range of systems 
types. Electrons are described quantum-mechanically within 
Density-Functional Theory (DFT), in its time-dependent form 
(TDDFT) when doing simulations in time. Nuclei are described
classically as point particles. Electron-nucleus interaction
is described within the Pseudopotential approximation. 

%package devel
Summary:        Octopus development headers & libraries
License:        GPLv2+
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
This package contains the development headers for Octopus.

%prep
%setup -q
sed -i -e '218,220d' -e '222,224d' src/basic/global.F90

%build
%ifarch x86_64
  %configure CFLAGS="-g -O2 -fPIE -fPIC -msse4.1 -Wno-line-truncation"
%else
  %configure CFLAGS="-g -O2 -fPIE -fPIC -Wno-line-truncation"
%endif
#./configure FCCPP="/lib/cpp -std=gnu++14 -xc++" FCFLAGS_LIBXC="-I/usr/include -I%{_libdir}/gfortran/modules" \
#FCFLAGS="-ffree-line-length-none -fallow-argument-mismatch -fallow-invalid-boz" \
#       --host=%{_host} --build=%{_build} \
#        --target=%{_target_platform} \
#        --program-prefix=%{?_program_prefix} \
#        --prefix=%{_prefix} \
#        --exec-prefix=%{_exec_prefix} \
#        --bindir=%{_bindir} \
#        --sbindir=%{_sbindir} \
#        --sysconfdir=%{_sysconfdir} \
#        --datadir=%{_datadir} \
#        --includedir=%{_includedir} \
#        --libdir=%{_libdir} \
#        --libexecdir=%{_libexecdir} \
#        --localstatedir=%{_localstatedir} \
#        --sharedstatedir=%{_sharedstatedir} \
#        --mandir=%{_mandir} \
#        --infodir=%{_infodir} --disable-static

%make_build -j 1

%install
rm -rf %{buildroot}
%make_install
#install -Dm644 /root/rpmbuild/BUILDROOT/octopus-*/liboct_parser.a %{buildroot}%{_libdir}/liboct_parser.a

%post
install-info %{_infodir}/octopus.info &> /dev/null

%preun
install-info --remove octopus &> /dev/null

%files
%doc README COPYING AUTHORS
%{_bindir}/*
%{_datadir}/octopus
%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/*.a

%changelog
* Sun Sep 25 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 12.0
- Rebuilt for Fedora
* Mon Sep 29 2008 Jussi Lehtola - 3.0.1-4
- Devel provides -static.
- Change defattrs to (-,root,root,-).
* Mon Sep 29 2008 Jussi Lehtola - 3.0.1-3
- Branch headers and .a files to -devel.
- Branch MPI binaries to MPI package.
- Add gcc-gfortran >= 4.3 to build reqs.
* Mon Sep 29 2008 Jussi Lehtola - 3.0.1-2
- Implement out-of-tree builds.
- Add smpflags to make.
* Sun Sep 28 2008 Jussi Lehtola - 3.0.1-1
- Initial release
