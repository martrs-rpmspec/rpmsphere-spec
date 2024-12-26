Summary:      An APL interpreter
Name:         apl
Version:      1.9
Release:      1
Group:        Applications/Interpreters
Source:       https://ftp.gnu.org/gnu/apl/apl-%{version}.tar.gz
License:      GPL
BuildRequires: readline-devel
BuildRequires: lapack-devel

%description
An APL interpreter (mostly) according to ISO/IEC Standard 13751
aka. "Programming Language APL, Extended"

%prep
%setup -q

%build
export CXX_WERROR=no
%configure
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%files
%{_bindir}/*
%{_libdir}/apl
%{_docdir}/*
%{_infodir}/*
%{_mandir}/*
%{_sysconfdir}/gnu-apl.d

%changelog
* Sun Dec 08 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 1.9
- Rebuilt for Fedora
