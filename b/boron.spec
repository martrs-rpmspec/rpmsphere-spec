%undefine _debugsource_packages

Summary: Scripting language and C library useful for building DSLs
Name: boron
Version: 2.1.0
Release: 1
License: LGPLv3+
URL: https://urlan.sf.net/boron
Group: Development/Languages
Source: boron-%{version}.tar.gz
BuildRequires: zlib-devel

%description
Boron is an interpreted, prototype-based, scripting language similar to Rebol.
The interpreter and datatype system is a C library useful for building
domain specific languages embedded in C/C++ applications.

%prep
%setup -q
#ifarch aarch64
#sed -i 243d eval/console.c
#endif

%build
./configure --thread --timecode --gnu-readline
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}/usr VER=%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README.md LICENSE* ChangeLog
%{_mandir}/man1/%{name}*
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so*

%changelog
* Sun Apr 07 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 2.1.0
- Rebuilt for Fedora
* Fri Mar 16 2012 Karl Robillard <wickedsmoke@users.sf.net>
- No longer using cmake.
* Fri Dec  4 2009 Karl Robillard <wickedsmoke@users.sf.net>
- Initial package release.
