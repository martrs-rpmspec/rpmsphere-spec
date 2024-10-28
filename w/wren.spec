%undefine _debugsource_packages

Summary: Wren programming language
Name: wren
Version: 0.4.0
Release: 1
License: MIT
Group: Development/Languages
Source: https://github.com/munificent/wren/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
URL: https://github.com/munificent/wren
#BuildRequires: libuv-static
#BuildRequires: gyp
#BuildRequires: python3

%description
Wren is a small, fast, class-based concurrent scripting language.
Think Smalltalk in a Lua-sized package with a dash of Erlang and
wrapped up in a familiar, modern syntax.

%prep
%setup -q
#sed -i 's|LIBUV_DIR :=.*|LIBUV_DIR := /usr|' util/wren.mk
#sed -i 's|LIBUV     :=.*|LIBUV     := %{_libdir}/libuv.a|' util/wren.mk
#sed -i '/libuv.py/d' util/wren.mk
#sed -i 's|-fPIC|-fPIC -Wno-error|' Makefile util/wren.mk
#sed -i 's|sprintf(message,|snprintf(message, sizeof(message),|' src/vm/wren_compiler.c
sed -i 's|wren_test|wren|' test/test.c
sed -i 's| -m64||' projects/*/*.make

%build
make -C projects/make

%install
rm -rf $RPM_BUILD_ROOT
install -Dm755 bin/%{name}_test %{buildroot}%{_bindir}/%{name}

%files 
%doc *.md AUTHORS LICENSE
%{_bindir}/%{name}

%changelog
* Sun Apr 11 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 0.4.0
- Rebuilt for Fedora
