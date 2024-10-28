Name:           oorexx
Version:        5.1.0.12831
Release:        1
Summary:        Open Object Rexx
Group:          Development/Languages
License:        CPL
URL:            https://www.oorexx.org
Source0:        https://switch.dl.sourceforge.net/sourceforge/oorexx/oorexx-5.1.0-12831.tar.gz
Source1:        https://switch.dl.sourceforge.net/sourceforge/oorexx/ooRexx-5.1.0beta-pdf.zip
Patch0:         oorexx-4.2.0-paths.patch
Patch1:         oorexx-4.2.0-gcc6.patch
BuildRequires:  byacc

%description
Open Object Rexx is an object-oriented scripting language. The
language is designed for "non-programmer" type users, so it is easy to
learn and easy to use, and provides an excellent vehicle to enter the
world of object-oriented programming without much effort.

It extends the procedural way of programming with object-oriented
features that allow you to gradually change your programming style as
you learn more about objects.

%package libs
Summary:        Libraries for ooRexx
Group:          System Environment/Libraries

%description libs
Libraries for ooRexx.

%package docs
Summary:        Documentation for ooRexx
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description docs
Documentation for ooRexx.

%package devel
Summary:        Header files and libraries for ooRexx
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Header files and libraries for ooRexx.

%prep
%setup -q -n %{name}-5.1.0-12831 -a 1
#unzip -qo %{SOURCE1}
#patch0 -p1 -b .paths
#patch1 -p1 -b .gcc6

%build
#configure --disable-static
#sed -i -e 's,-O2,-std=gnu++11 -fpermissive,g' -e 's|-Werror=format-security||g' Makefile
#make %{?_smp_mflags}
%{cmake}
%{cmake_build}

%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
#find $RPM_BUILD_ROOT -name '*.la' -exec rm -f '{}' ';'
#rm -fr samples/**/.deps
#rm -f $RPM_BUILD_ROOT%{_datadir}/ooRexx/rexx.csh
#rm -f $RPM_BUILD_ROOT%{_datadir}/ooRexx/rexx.sh
#chmod 0644 $RPM_BUILD_ROOT%{_datadir}/ooRexx/*

# remove cruft
#rm -f $RPM_BUILD_ROOT%{_datadir}/ooRexx/{*.rex,readme}
#find . -name .deps | xargs rm -fr
#rm -fr samples/windows
%{cmake_install}

%files
%doc CPLv1.0.txt CHANGES CONTRIBUTORS NOTICE readme.version
%{_bindir}/*
%{_datadir}/ooRexx
%{_mandir}/man*/*

%files docs
%doc *.pdf
%doc samples ReleaseNotes

%files devel
%{_includedir}/*
#{_bindir}/oorexx-config
%{_libdir}/*.so

%files libs
%{_libdir}/lib*.so.*
%{_libdir}/rexx.img

%changelog
* Sun Apr 21 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 5.1.0.12831
- Rebuilt for Fedora
* Mon Oct 10 2016 Gérard Milmeister <gemi@bluewin.ch> - 4.2.0-3
- Patch for gcc6
- Disable optimization, which breaks the build using gcc6
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Thu Jul  9 2015 Gérard Milmeister <gemi@bluewin.ch> - 4.2.0-1
- new release 4.2.0
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
* Sat Feb  5 2011 Gérard Milmeister <gemi@bluewin.ch> - 4.1.0-2
- added BuildRequires byacc
* Sat Feb  5 2011 Gérard Milmeister <gemi@bluewin.ch> - 4.1.0-1
- new release 4.1.0
* Sun Aug  9 2009 Gerard Milmeister <gemi@bluewin.ch> - 4.0.0-2.4801
- moved .so libraries to -libs
* Sat Aug  8 2009 Gerard Milmeister <gemi@bluewin.ch> - 4.0.0-1.4801
- new release 4.0.0
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 3.2.0-4
- fix for GCC 4.3
* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.0-3
- Autorebuild for GCC 4.3
* Sat Dec  1 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.2.0-2
- exclude arch ppc64
* Sat Dec  1 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.2.0-1
- new release 3.2.0
* Sun Dec  3 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.1.1-1
- new version 3.1.1
* Tue Oct 10 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.1.0-5
- Exclude x86_64
* Mon Oct  9 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.1.0-4
- Build exclusively on i386 for now
* Mon Sep 25 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.1.0-1
- new version 3.1.0
* Tue May  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.0.0-1
- First Fedora release
