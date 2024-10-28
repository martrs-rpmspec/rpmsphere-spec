%define __python /usr/bin/python2
Name:          morpyon
Version:       2.0.1
Release:       1
Summary:       A game where you must align 5 pieces on a board
Group:         Graphical Desktop/Applications/Games
URL:           https://flibuste.net/libre/morpyon/
Source0:       https://flibuste.net/libre/morpyon/Morpyon-%{version}.tar.gz
Source1:       morpyon.desktop
Patch0:         morpyon-2.0.1-path.patch
License:       GPL
BuildRequires: python2-devel
BuildRequires: pygame-devel
Requires:      pygame
BuildArch:     noarch

%description
Morpyon (also known as "gomoku") is a game where you must align 5 pieces
on a board against a computer opponent.

%prep
%setup -q -n Morpyon-%{version}
%patch 0 -p1

%build
python2 setup.py build

%install
rm -rf %{buildroot}
python2 setup.py install \
   --root=%{buildroot} \
   --install-headers=%{_includedir}/python \
   --install-lib=%{python_sitearch} \
   --install-data=%{_datadir}/%{name}

install -D -m755 morpyon.py %{buildroot}%{_bindir}/morpyon.py
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

sed -i 's|/usr/bin/env python$|/usr/bin/python2|' %{buildroot}%{_bindir}/*
sed -i 's|/usr/bin/python$|/usr/bin/python2|' %{buildroot}%{_bindir}/*

%files
%{_bindir}/morpyon_pygame.py
%{_bindir}/morpyon.py
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{python2_sitearch}/Morpyon-%{version}-py*.egg-info

%changelog
* Tue Mar 20 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 2.0.1
- Rebuilt for Fedora
* Sat Oct 17 2009 Silvan Calarco <silvan.calarco@mambasoft.it> 2.0.1-5mamba
- specfile updated and rebuilt with python 2.6
* Fri Dec 23 2005 Davide Madrisan <davide.madrisan@qilinux.it> 2.0.1-4qilnx
- new desktop file
* Wed Aug 17 2005 Massimo Pintore <massimo.pintore@qilinux.it> 2.0.1-3qilnx
- library directory changed from %%{_libdir}/python to %%{_libdir}/site-python
* Wed Jul 27 2005 Massimo Pintore <massimo.pintore@qilinux.it> 2.0.1-2qilnx
- added missing requires (python-pygame)
* Tue Jul 26 2005 Massimo Pintore <massimo.pintore@qilinux.it> 2.0.1-1qilnx
- package created by autospec
