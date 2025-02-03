%global _name pam-python

Name:           pam_python
Version:        1.0.8
Release:        1
Group:          System/Libraries
URL:            https://pam-python.sourceforge.net
License:        AGPLv3+
Summary:        Support for writing PAM modules in Python
Source:         https://sourceforge.net/projects/%{_name}/files/%{_name}-%{version}-1/%{_name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  pam-devel
#BuildRequires: python2-sphinx

%description
pam-python is a PAM Module that runs the Python interpreter, thus allowing PAM
modules to be written in Python.

%prep
%setup -q -n %{_name}-%{version}
sed -i 's|-Werror|-Wno-implicit-function-declaration|' src/Makefile
sed -i 's|python2|python3|' src/setup.py
sed -i 's|cp build/lib.*/pam_python.so $(DESTDIR)$(LIBDIR)|cp build/lib.*/pam_python.*.so $(DESTDIR)$(LIBDIR)/pam_python.so|' src/Makefile

%build
make -C src

%install
make -C src install LIBDIR=%{buildroot}/%{_lib}/security

%files
%doc *.txt *.html
/%{_lib}/security/pam_python.so

%changelog
* Fri Jan 17 2025 Wei-Lun Chao <bluebat@member.fsf.org> - 1.0.8
- Rebuilt for Fedora
* Wed Sep 14 2016 mitya <mitya> 1.0.6-1.mga6
+ Revision: 1052577
- pam-python 1.0.6
- Created package structure for pam-python.
