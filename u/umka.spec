%undefine _debugsource_packages

Summary: A statically typed embeddable scripting language
Name: umka
Version: 1.2
Release: 1
License: BSD-2
Group: Development/Languages
Source: https://github.com/vtereshkov/umka-lang/archive/v%{version}.tar.gz#/%{name}-lang-%{version}.tar.gz
URL: https://github.com/vtereshkov/umka-lang

%description
Umka is a statically typed embeddable scripting language. It combines
the simplicity and flexibility needed for scripting with a compile-time
protection against type errors. Its aim is to follow the Python Zen
principle Explicit is better than implicit more consistently than
dynamically typed languages generally do.

%prep
%setup -q -n %{name}-lang-%{version}
%ifarch aarch64
sed -i 's|-malign-double||' Makefile
%endif

%build
%make_build

%install
rm -rf $RPM_BUILD_ROOT
install -Dm755 build/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm755 build/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so
install -Dm644 build/lib%{name}.a %{buildroot}%{_libdir}/lib%{name}.a
install -Dm644 src/%{name}_api.h %{buildroot}%{_includedir}/%{name}_api.h
install -d %{buildroot}%{_datadir}/%{name}
cp -a Umka.sublime-syntax %{buildroot}%{_datadir}/%{name}

%files 
%doc *.md LICENSE examples doc/*
%{_bindir}/%{name}
%{_libdir}/lib%{name}.*
%{_includedir}/%{name}_api.h
%{_datadir}/%{name}

%changelog
* Sun Nov 12 2023 Wei-Lun Chao <bluebat@member.fsf.org> - 1.2
- Rebuilt for Fedora
