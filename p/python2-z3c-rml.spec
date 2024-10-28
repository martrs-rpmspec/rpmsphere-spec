Name:          python2-z3c-rml
Version:       0.9.1
Release:       6.1
Summary:       An alternative implementation of RML
Group:         System/Libraries/Python
URL:           https://pypi.python.org/pypi/z3c.rml
Source:        https://pypi.python.org/packages/source/z/z3c.rml/z3c.rml-%{version}.tar.gz
License:       Zope Public License
BuildRequires: python2-setuptools
BuildRequires:  python2
Requires:      python2-reportlab
Requires:      python2-zope-schema
Requires:      python2-lxml
BuildArch:     noarch

%description
z3c.rml is an alternative implementation of ReportLab's RML PDF generation XML format.
Like the original implementation, it is based on ReportLab's reportlab library.

%prep
%setup -q -n z3c.rml-%{version}

%build
python2 setup.py build

%install
rm -rf "$RPM_BUILD_ROOT"
python2 setup.py install \
   -O1 --skip-build \
   --root="$RPM_BUILD_ROOT" \
   --install-headers=%{_includedir}/python2.7 \
   --install-lib=%{python2_sitelib} \
   --single-version-externally-managed \
   --record=%{name}.filelist

#sed -i "\,\.egg-info/,d;s,.*/man/.*,&.gz," %{name}.filelist

echo "#!/bin/sh" > rml2pdf.sh
echo exec "python2" "%{python2_sitelib}/z3c/rml/rml2pdf.py" "\$@" >> rml2pdf.sh
install -D -m 755 rml2pdf.sh \
   $RPM_BUILD_ROOT%{_bindir}/rml2pdf
echo "%{_bindir}/rml2pdf" >> %{name}.filelist

sed -i 's|/usr/bin/python$|/usr/bin/python2|' %{buildroot}%{_bindir}/*

%files -f %{name}.filelist
%doc AUTHORS.txt CHANGES.txt README.txt TODOS.txt

%changelog
* Mon Jun 13 2011 Wei-Lun Chao <bluebat@member.fsf.org> - 0.9.1
- Rebuilt for Fedora
* Wed Oct 13 2010 Stefano Cotta Ramusino <stefano.cotta@openmamba.org> 0.9.1-1mamba
- package created by autospec
