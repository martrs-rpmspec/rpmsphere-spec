Name:           arping
Version:        2.23
Release:        1
Summary:        Ethernet Layer 2 ping tool
Group:          Applications/Internet
License:        GPLv2+
URL:            https://www.habets.pp.se/synscan/programs.php?prog=arping
Source0:        https://www.habets.pp.se/synscan/files/%{name}-%{version}.tar.gz
BuildRequires:  libpcap-devel
BuildRequires:  libnet-devel

%description
Arping is a util to find out it a specific IP address on the LAN is
'taken' and what MAC address owns it. Sure, you could just use
'ping' to find out if it's taken and even if the computer blocks ping
(and everything else) you still get an entry in your ARP cache.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
install -Dp -m 4755 src/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}-habets
install -Dp -m 0644 doc/%{name}.8 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}-habets.1
#Remove exec permisson from script
chmod -x extra/arping-scan-net.sh

%files
%doc LICENSE README extra/arping-scan-net.sh
%{_mandir}/man*/%{name}-habets*.*
%{_bindir}/%{name}-habets

%changelog
* Sun May 8 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 2.23
- Rebuilt for Fedora
* Tue Dec 23 2008 Fabian Affolter <fabian@bernewireless.net> - 2.08-1
- Initial spec for Fedora
