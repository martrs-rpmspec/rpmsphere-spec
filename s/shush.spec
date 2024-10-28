%undefine _auto_set_build_flags

Name:         shush
Summary:      Shell Command Logging Wrapper
URL:          https://web.taranis.org/shush/
Group:        System
License:      BSD
Version:      1.2.3
Release:      7.1
Source0:      https://web.taranis.org/shush/dist/shush-%{version}.tgz

%description
shush(1) runs a command and optionally reports its output by mail.
It is a useful wrapper around cron jobs.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --with-pcre=%{_prefix} \
    --build=x86_64 \
    --without-syslog
%{__make} %{_smp_mflags -O}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} %{_smp_mflags} install \
    prefix=$RPM_BUILD_ROOT%{_prefix} \
    exec_prefix=$RPM_BUILD_ROOT%{_prefix} \
    mandir=$RPM_BUILD_ROOT%{_mandir}

%files
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Sep 25 2013 Wei-Lun Chao <bluebat@member.fsf.org> - 1.2.3
- Rebuilt for Fedora
