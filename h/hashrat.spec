%global _name Hashrat

Name: hashrat
Summary: Hashing tool supporting several hashes and recursivity
Version: 1.23
License: GPLv3
Release: 1
Group: utils
URL: https://www.cjpaget.co.uk/Code/Hashrat
Source0: https://codeload.github.com/ColumPaget/%{_name}/tar.gz/%{version}/%{_name}-%{version}.tar.gz

%description
Hashrat is a hash-generation utility that supports the md5, sha1, sha256,
sha512, whirlpool, jh-244, jh256, jh-384 and jh-512 hash functions, and
also the HMAC versions of those functions. It can output in 'traditional'
format (same as md5sum and shasum and the like), or it's own format.

Hashes can be output in octal, decimal, hexadecimal, uppercase hexadecimal
or base64. Hashrat also supports directory recursion, hashing entire devices,
generating a hash for an entire directory, operations in remote machines
and several other features. It has a 'CGI' mode that can be used as a
web-page to lookup hashes. This tool is useful in forensics investigations
and network security.

%prep
%setup -q -n %{_name}-%{version}
sed -i 's|runstatedir|runstate|g' configure

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%doc LICENSE README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Dec 12 2024 Wei-Lun Chao <bluebat@member.fsf.org> - 1.23
- Rebuilt for Fedora
