%global __os_install_post %{nil}

Summary: Adjustable data format binary editor
Name: bed
Version: 3.1.2
License: GPL
Release: 1
Source: https://www.dse.nl/~bed/download/bed-%{version}.src.tar.xz
URL: https://sourceforge.net/projects/binaryeditor/
Group: Applications/Editors

%description 
Adjustable data format binary editor. Data formats are
ASCII, unsigned and signed integers, float, bit-flags,
bit-fields, labels, ebcdic and time_t. Different sizes
and byte orderings are possible. Data types can
be used in structures. Other data formats, filters and
procedures can be defined in plugins. Contains copy,
past, undo, redo, search, replace, marks, record/play and
context sensitive help. Raw edit of hard drives. Under  
Linux and FreeBSD even usable without X window.

%prep
%setup -q
sed -i '34i #include <algorithm>' src/search.cpp

%build
#export CXXFLAGS="-Wno-c++11-narrowing"
#make realclean
#make linuxconfig
#s/^[^%]*%_\([^         ]*\)[   ].*$/--\1=%{_\1} /g
./configure       --prefix=%{_prefix} --exec_prefix=%{_exec_prefix} --bindir=%{_bindir} --datadir=%{_datadir} --libdir=%{_libdir} --mandir=%{_mandir} 
make dep
sed -i 's|-fPIC|-fPIC -Wno-c++11-narrowing|' plugins/examples/Makefile
make

%install
make  installfiles ROOTDIR=$RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_libdir}/%{name}-%{version}
%exclude %{_datadir}/applications/%{name}-binary-editor.desktop
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Sun Dec 8 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 3.1.2
- Rebuilt for Fedora
