Name:      tarmux
Version:   1.0.4
Release:   1
Summary:   Multiplex / demultiplex streams
License:   ASL 2.0
Group:     Applications/System
Source:    https://github.com/minfrin/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
URL:       https://github.com/minfrin/tarmux
BuildRequires: libarchive-devel >= 3, help2man, gcc

%define    __libtoolize /bin/true

%description
Multiplex and demultiplex streams using tar file fragments.

%prep
%setup -q
rm -rf %{_builddir}/%{name}-%{version}/debian
%build
%configure
%make_build

%install
%make_install

%files
%{_bindir}/tardemux
%{_bindir}/tarmux
%{_mandir}/man1/tardemux.1*
%{_mandir}/man1/tarmux.1*
%doc AUTHORS ChangeLog README
%license COPYING

%changelog
* Sun Dec 12 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 1.0.4
- Rebuilt for Fedora
* Mon May 23 2016 Graham Leggett <minfrin@sharp.fm> - 1.0.1-1
- Updates to packaging
* Sun May 22 2016 Graham Leggett <minfrin@sharp.fm> - 1.0.0-1
- Initial version of the package
