Name:           sagan
Version:        2.0.2
Release:        1
#Source:         %{name}-%{name}-%{version}.tar.gz 
Source:		%{name}-v-2-0.2.tar.gz
License:        GPLv2
Group:          System/Daemons
Summary:        Real time system and event log monitoring system
URL:            https://sagan.quadrantsec.com/
BuildRequires:  pcre-devel
BuildRequires:  postgresql-devel
BuildRequires:  libesmtp-devel
BuildRequires:  json-c-devel
BuildRequires:  libfastjson-devel
BuildRequires:  liblognorm-devel

%description
Sagan is a multi-threaded, real time system and event log monitoring system,
but with a twist. Sagan uses a "Snort" like rule set for detecting bad
things happening on your network and/or computer systems. If Sagan detects
a "bad thing" happening, that event can be stored to a Snort database
(MySQL/PostgreSQL) and Sagan will attempt to correlate the event with your
Snort Intrusion Detection/Intrusion Prevention (IDS/IPS) system.

%prep
%setup -q -n %{name}-v-2-0.2
sed -i '59i #include <inttypes.h>' src/config-yaml.c
sed -i '36i #include <inttypes.h>' src/tracking-syslog.c

%build
export LDFLAGS=-Wl,--allow-multiple-definition
./autogen.sh
%ifarch %ix86
sed -i 's|\(sse.*\)=yes|\1=no|' configure
%endif
%configure --disable-mysql --disable-prelude --disable-libpcap --disable-libdnet --enable-lognorm
sed -i 's|-I/usr/include/libfastjson|-I/usr/include/libfastjson -I/usr/include/liblognorm|' `find . -name Makefile`
%{__make} %{?_smp_flags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/groupadd -g 66 -o -r sagan 2> /dev/null || :

%{_sbindir}/useradd -r -o -g sagan -u 66 -s /bin/false -c "sagan monitor daemon" \
        -d /home/sagan sagan 2> /dev/null || :

%files
%doc TODO COPYING 
%{_bindir}/sagan
#{_sbindir}/sagan
%config %{_sysconfdir}/sagan.yaml
%{_datadir}/man/man?/sagan.*

%changelog
* Sun Nov 12 2023 Wei-Lun Chao <bluebat@member.fsf.org> - 2.0.2
- Rebuilt for Fedora
* Mon Jun 28 2010 Matthias Weckbecker <mweckbecker@suse.de>
- add sagan user && group
* Mon Jun 28 2010 mweckbecker@novell.com
- changed group to "Systems/Daemons"
* Mon Jun 28 2010 mweckbecker@novell.com
- strip sagan binary, removed zero-size documentation
* Mon Jun 28 2010 mweckbecker@novell.com
- added patch to fix implicit usage of functions, bzipped source
* Mon Jun 28 2010 mweckbecker@novell.com
- patch renamed
* Mon Jun 28 2010 mrueckert@suse.de
- fixing package
