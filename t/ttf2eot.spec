Name:         ttf2eot
Summary:      TTF to EOT Font Format Conversion Tool
URL:          https://ttf2eot.googlecode.com/
Group:        Typesetting
License:      GPL
Version:      0.0.2.2
Release:      4.1
Source0:      https://ttf2eot.googlecode.com/files/ttf2eot-0.0.2-2.tar.gz
Patch0:        ttf2eot.patch

%description
ttf2eot is a small utility fort converting TrueType Fonts (TTF)
to EOT (Embedded OpenType) fonts as used by Internet Explorer
when using the CSS "@font-face" feature. The code is derived from
Chromium's WebKit derived code base.

%prep
%setup -q -n ttf2eot-0.0.2-2
%patch 0 -p0

%build
%{__make} %{_smp_mflags} CXX="%{__cxx}" CXXFLAGS="%{optflags} -Wno-multichar"

%install
mkdir -p -m 755 \
    $RPM_BUILD_ROOT%{_bindir}
install -c -m 755 \
    ttf2eot $RPM_BUILD_ROOT%{_bindir}

%files
%{_bindir}/%{name}

%changelog
* Wed Sep 25 2013 Wei-Lun Chao <bluebat@member.fsf.org> - 0.0.2.2
- Rebuilt for Fedora
