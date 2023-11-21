Name:       ibus-array
Version:    0.2.2
Release:    2
Summary:    IBus Array30 engine
License:    GPLv3
Group:      System Environment/Libraries
URL:        https://github.com/lexical/ibus-array
#Source0:    https://github.com/lexical/ibus-array/archive/release-%{version}.tar.gz#/%{name}-release-%{version}.tar.gz
Source0:    %{name}-master.zip
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  ibus-devel
BuildRequires:  sqlite-devel
Requires:   ibus

%description
The Array30 engine for IBus to input Hanzi.

%prep
#setup -q -n %{name}-release-%{version}
%setup -q -n %{name}-master

%build
#autoreconf -ifv
sed -i 's|-g -O0|$CFLAGS|' autogen.sh
./autogen.sh --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
ibus restart || :

%postun
ibus restart || :

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README NEWS ChangeLog
%{_datadir}/ibus-array
%{_libexecdir}/ibus-engine-array
%{_libexecdir}/ibus-setup-array
%{_datadir}/ibus/component/array.xml

%changelog
* Thu Jul 01 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 0.2.2
- Update to 0.2.2 git
* Wed Apr 22 2009 Yu-Chun Wang <mainlander1122@gmail.com> - 0.0.1
- The first version
