Name:           python2-whiteboard
Version:        1.0.3
Release:        1
Summary:        Linux whiteboard in python
License:        open source
URL:            https://github.com/pnegre/python-whiteboard
Group:          User Interface/X Hardware Support
#Source0:       python-whiteboard-%{version}.tar.gz
Source0:        python-whiteboard-master.zip
BuildRequires:  qt4-devel
Requires:       pybluez, PyQt4, numpy, cwiid-python2, python2-xlib
BuildArch:      noarch

%description
Python-whiteboard is a program that lets you build your own
electronic whiteboard. You only need a wii remote and a IR pen.

%prep
%setup -q -n python-whiteboard-master
sed -i 's/lrelease/lrelease-qt4/' makefile

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
echo -e 'Name[zh_TW]=Python-Whiteboard\nComment[zh_TW]=以 Wiimote 控制滑鼠指標' >> $RPM_BUILD_ROOT%{_datadir}/applications/python-whiteboard.desktop
sed -i 's/Application;Education/HardwareSettings;Settings;/' $RPM_BUILD_ROOT%{_datadir}/applications/python-whiteboard.desktop

sed -i 's|/usr/bin/python$|/usr/bin/python2|' %{buildroot}%{_bindir}/*

%files
%doc License.txt README debian/changelog
%{_bindir}/*
%{_datadir}/applications/python-whiteboard.desktop
%{_datadir}/python-whiteboard
%{_datadir}/pixmaps/*
%{_datadir}/qt4/translations/*

%changelog
* Sun Mar 20 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 1.0.3
- Rebuilt for Fedora
