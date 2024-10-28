%undefine _debugsource_packages

Name:           connectagram
Summary:        Anagram game
Version:        1.3.1
Release:        1
License:        GPL-3.0+
URL:            https://gottcode.org/%{name}/
Source:         https://gottcode.org/%{name}/%{name}-%{version}-src.tar.bz2
Group:          Amusements/Games
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  qt5-qtbase-devel

%description
A word unscrambling game. The board consists of several scrambled words that
are joined together. You can choose the length of the words, the amount of
words, and the pattern that the words are arranged in. The game provides a
hint option for times when you are stuck, and features an online word lookup
that fetches the definitions of each word from Wiktionary. Your current
progress is automatically saved.

%prep
%setup -q

%build
CXXFLAGS="%{optflags}" qmake-qt5 PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
make INSTALL_ROOT=%{buildroot} install
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc ChangeLog CREDITS
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_mandir}/man6/%{name}.6.gz
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}.xpm

%changelog
* Sun Oct 24 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 1.3.1
- Rebuilt for Fedora
* Sun May  5 2013 Graeme Gott <graeme@gottcode.org>
- version 1.1.1-1
- Update to 1.1.1
  - Added missing game data.
  - Added German and Greek translations.
* Wed Feb 20 2013 Graeme Gott <graeme@gottcode.org>
- version 1.1.0.1-1
- Added missing program icons.
* Wed Feb 20 2013 Graeme Gott <graeme@gottcode.org>
- version 1.1.0-1
- Update to 1.1.0
  - Added dragging board to scroll
  - Added French wordlist
  - Use definitions from Wiktionary
  - Improved new game dialog
  - Added French, Romanian, Russian translations
  - Added support for Qt 5
* Thu Jan 24 2013 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-10
- Remove nonexistent COPYING from spec file.
* Thu Jan 24 2013 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-9
- Remove nonexistent xpm from spec file.
* Thu Jan 24 2013 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-8
- Add category to desktop file.
* Thu Jan 24 2013 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-7
- Improve spec file.
* Mon Jan 21 2013 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-6
- Add Debian packaging.
* Mon Dec  5 2011 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-5
- Update GNOME icon cache.
* Fri Nov 11 2011 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-4
- Improve spec file.
* Sat Apr  2 2011 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-3
- Add dependency on hicolor-icon-theme.
* Wed Sep 22 2010 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-2
- Fixed build issue on openSUSE 11.2.
* Tue Sep 21 2010 Graeme Gott <graeme@gottcode.org>
- version 1.0.1-1
- Initial package.
