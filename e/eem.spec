%undefine _debugsource_packages
Summary:        Enlightenment for Embedded
Name:           eem
Version:        20100507
Release:        1
License:        unknown
Group:          Graphical desktop/Enlightenment
URL:            https://www.rasterman.com/files/eem.avi
Source0:        https://people.profusion.mobi/~gustavo/%{name}.tgz
Source1:        %{name}.desktop
Source2:        %{name}.sh
Patch0:         evas_smart_class_new.patch
BuildRequires:  ecore-devel, evas-devel, edje

%description
Enlightenment for Embedded Device.

%prep
%setup -q -n %{name}
%patch 0 -p1
rm -f data/edjes/default.edj
sed -i 's|-lm|-lm -leina|' Makefile

%build
%__make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a %{name} data $RPM_BUILD_ROOT%{_datadir}/%{name}
install -Dm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
install -Dm 755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Mar 20 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 20100507
- Rebuilt for Fedora
