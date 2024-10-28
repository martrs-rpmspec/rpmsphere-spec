Name: nubasic
Summary: BASIC language interpreter written in C++11 for educational purposes
Version: 1.52
Release: 1
Group: Development/Language
License: GPLv2+
URL: https://github.com/eantcal/nubasic
Source0: https://downloads.sourceforge.net/project/%{name}/%{name}-rel_%{version}.tar.gz
BuildRequires: gcc-c++ automake
BuildRequires: libX11-devel
#BuildRequires: xterm

%description
nuBASIC has been designed mainly for educational purposes both for C++ developers that
can deal with a non-trivial example of C++11 programming and for nuBASIC's users,
that may get hooked on programming.
As the name suggests, nuBASIC is a programming language from the BASIC family.
Anyone who has previously worked with other BASIC languages will quickly become accustomed to nuBASIC.
Large sections of the basic constructs of nuBASIC are compatible with other Basic dialects.
nuBASIC can be used by any user without any additional programs.
It has the components needed to create programs, including:
- The command line interpreter (CLI), which provides an inline-editor for creating and testing programs.
- The language interpreter, which is needed to run nuBASIC programs

%prep
%setup -q -n %{name}-rel_%{version}
sed -i -e 's|-std=c++14||' -e 's|-Wall|-Wall -fPIE|' `find . -name CMakeLists.txt`
#sed -i '9i #include <string>' lib/nu_playsnd.cc
sed -i '18i #include <cstddef> ' include/nu_flag_map.h
sed -i 's|static volatile gsize|static gsize|' ide/scintilla/gtk/ScintillaGTKAccessible.cxx

%build
%cmake .
%cmake_build

%install
%cmake_install

%files
%doc AUTHORS ChangeLog README NEWS THANKS
%{_bindir}/%{name}*
#{_libdir}/lib%{name}.a

%changelog
* Sun Sep 04 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 1.52
- Rebuilt for Fedora
* Thu Sep 11 2014 Fedora 20 Release <acaldmail@gmail.com> - 1.19
- Rebuild RPM for Fedora distros
