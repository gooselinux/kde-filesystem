%define _kde4_prefix %_prefix
%define _kde4_sysconfdir %_sysconfdir
%define _kde4_libdir %_libdir
%define _kde4_libexecdir %_libexecdir/kde4
%define _kde4_datadir %_datadir
%define _kde4_sharedir %_datadir
%define _kde4_iconsdir %_kde4_sharedir/icons
%define _kde4_configdir %_kde4_sharedir/config
%define _kde4_appsdir %_kde4_sharedir/kde4/apps
%define _kde4_docdir %_kde4_prefix/share/doc
%define _kde4_bindir %_kde4_prefix/bin
%define _kde4_sbindir %_kde4_prefix/sbin
%define _kde4_includedir %_kde4_prefix/include/kde4
%define _kde4_buildtype release
%define _kde4_macros_api 2

%if 0%{?fedora} > 11 || 0%{?rhel} >= 6
# see http://bugzilla.redhat.com/515745
%define exclude_sounds 1
%endif

Summary: KDE filesystem layout
Name: kde-filesystem
Version: 4
Release: 30.1%{?dist}

Group: System Environment/Base
License: Public Domain
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

# teamnames (locales) borrowed from kde-i18n packaging
Source1: teamnames

Source2: macros.kde4
# increment whenever dirs change in an incompatible way
# kde4 apps built using macros.kde4 should

Source3: applnk-hidden-directory

Provides: kde4-macros(api) = %{_kde4_macros_api} 

BuildRequires: gawk

Requires:  filesystem
Requires:  rpm

%description
This package provides some directories that are required/used by KDE. 


%prep


%build


%install
rm -f $RPM_BUILD_DIR/%{name}.list
rm -rf $RPM_BUILD_ROOT

## KDE3 
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kde/{env,shutdown,kdm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/{applications/kde,applnk,apps,autostart,config,config.kcfg,emoticons,mimelnk,services,servicetypes,sounds,templates,source}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/apps/konqueror/servicemenus
# not sure who best should own locolor, so we'll included it here, for now. -- Rex
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applnk/{.hidden,Applications,Edutainment,Graphics,Internet,Settings,System,Toys,Utilities}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mimelnk/{all,application,audio,fonts,image,inode,interface,media,message,model,multipart,print,text,uri,video}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/en

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
 mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/common
 # do docs/common too, but it could be argued that apps/pkgs using or
 # depending on is a bug -- Rex
 mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/docs/
 ln -s ../common $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/docs/common
 echo "%lang($locale) %{_docdir}/HTML/$locale/" >> %{name}.list
done

# internal services shouldn't be displayed in menu
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/applnk/.hidden/.directory

## KDE4
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm \
      -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/env \
      -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/shutdown \
      -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/kdm \
      -p $RPM_BUILD_ROOT%{_kde4_includedir} \
      -p $RPM_BUILD_ROOT%{_kde4_libexecdir} \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/applications/kde4 \
      -p $RPM_BUILD_ROOT%{_kde4_appsdir} \
      -p $RPM_BUILD_ROOT%{_kde4_appsdir}/color-schemes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/autostart \
      -p $RPM_BUILD_ROOT%{_kde4_configdir} \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/config.kcfg \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/emoticons \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/services/ServiceMenus \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/servicetypes \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/templates/.source \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/16x16/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/16x16/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/16x16/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/22x22/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/22x22/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/22x22/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/32x32/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/32x32/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/32x32/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/48x48/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/48x48/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/48x48/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/sounds \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/wallpapers \
      -p $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/en/common

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
  mkdir -p $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/${locale}/common
  echo "%lang($locale) %{_kde4_docdir}/HTML/$locale/" >> %{name}.list
done

# rpm macros
cat >$RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.kde4<<EOF
%%_kde4_prefix %%_prefix
%%_kde4_sysconfdir %%_sysconfdir
%%_kde4_libdir %%_libdir
%%_kde4_libexecdir %%_libexecdir/kde4
%%_kde4_datadir %%_datadir
%%_kde4_sharedir %%_datadir
%%_kde4_iconsdir %%_kde4_sharedir/icons
%%_kde4_configdir %%_kde4_sharedir/config
%%_kde4_appsdir %%_kde4_sharedir/kde4/apps
%%_kde4_docdir %_kde4_prefix/share/doc
%%_kde4_bindir %%_kde4_prefix/bin
%%_kde4_sbindir %%_kde4_prefix/sbin
%%_kde4_includedir %%_kde4_prefix/include/kde4
%%_kde4_buildtype %_kde4_buildtype
%%_kde4_macros_api %_kde4_macros_api
EOF
cat %{SOURCE2} >> $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.kde4


%clean
rm -rf $RPM_BUILD_ROOT %{name}.list


%files -f %{name}.list
%defattr(-,root,root,-)

# KDE3
%{_sysconfdir}/kde/
%{_datadir}/applications/kde/
%{_datadir}/applnk/
%{_datadir}/apps/
%{_datadir}/autostart/
%{_datadir}/config/
%{_datadir}/config.kcfg/
%{_datadir}/emoticons/
%{_datadir}/icons/locolor
%{_datadir}/mimelnk/
%{_datadir}/services/
%{_datadir}/servicetypes/
%{?exclude_sounds:%exclude }%{_datadir}/sounds/
%{_datadir}/templates/
%dir %{_docdir}/HTML/
%lang(en) %{_docdir}/HTML/en/

# KDE4
%config /etc/rpm/macros.kde4
%{_kde4_sysconfdir}/kde/
%{_kde4_libexecdir}/
%{_kde4_includedir}/
%{_kde4_datadir}/applications/kde4/
%{_kde4_appsdir}/
%{_kde4_configdir}/
%{_kde4_sharedir}/config.kcfg/
%{_kde4_sharedir}/emoticons/
%{_kde4_sharedir}/kde4/
%{_kde4_sharedir}/templates/
%{_kde4_datadir}/autostart/
%{_kde4_datadir}/icons/locolor
%{?exclude_sounds:%exclude }%{_kde4_datadir}/sounds/
%{_kde4_datadir}/wallpapers/
%dir %{_kde4_docdir}/HTML/
%lang(en) %{_kde4_docdir}/HTML/en/


%changelog
* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 4-30.1
- Fix conditional for RHEL

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4-30
- kill the ownership of %%_datadir/sounds (#515745)

* Tue Aug 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4-29
- drop unused (and confusing) /etc/kde4/ crud

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Rex Dieter <rdieter@fedoraproject.org> 4-27
- Should own /usr/share/kde4/services/ServiceMenus (#505735)

* Mon May 11 2009 Rex Dieter <rdieter@fedoraproject.org> 4-26
- own %%_docdir/HTML/<lang>/{common,docs/common} (#445108)

* Thu Mar 12 2009 Rex Dieter <rdieter@fedoraproject.org> 4-25
- own %%_kde4_datadir/wallpapers (revert -20)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 08 2009 Rex Dieter <rdieter@fedoraproject.org> 4-23
- macros.kde4: use %%_cmake_lib_suffix64, %%_cmake_lib_suffix64

* Thu Dec 04 2008 Rex Dieter <rdieter@fedoraproject.org> 4-22
- macros.kde4: (re)add -DCMAKE_SKIP_RPATH:BOOL=ON

* Tue Dec 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4-21
- sync latest cmake macros
- macros.kde4: add -DCMAKE_VERBOSE_MAKEFILE=ON to %%cmake_kde4 (#474053)

* Wed Oct 08 2008 Than Ngo <than@redhat.com> 4-20
- /usr/share/wallpapers owned by desktop-backgrounds-basic

* Sat Sep 13 2008 Than Ngo <than@redhat.com> 4-19
- it's not needed to bump _kde4_macros_api
- use macro

* Sat Sep 13 2008 Than Ngo <than@redhat.com> 4-18
- remove redundant FEDORA, use CMAKE_BUILD_TYPE=release

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4-17
- + %%_kde4_sharedir/kde4

* Sun Jun 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4-16
- + %%_datadir/apps/konqueror(/servicemenus)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4-15
- omit %%_sysconfdir/kde/xdg (see also #249109)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-14
- don't define %%{_kde4_debug} in macros.kde4 anymore

* Wed Apr 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4-13
- define %%{_kde4_buildtype} in macros.kde4 too

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-12
- actually define %%{_kde4_libexecdir} in macros.kde4

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-11
- add %%{_kde4_libexecdir}, set LIBEXEC_INSTALL_DIR to it
- don't own %%{_kde4_libdir} which is just %%{_libdir}

* Mon Mar 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4-10
- macros.kde4: _kde4_buildtype=FEDORA

* Fri Mar 28 2008 Than Ngo <than@redhat.com>  4-9
- internal services shouldn't be displayed in menu, bz#321771

* Sun Jan 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4-8
- should not own %%_datadir/desktop-directories/ (#430420)

* Fri Jan 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-7
- own %%{_kde4_appsdir}/color-schemes

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4-6
- -Requires: redhat-rpm-config (revert 4-1 addition)

* Sun Dec 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4-5
- +%%_datadir/autostart, %%_kde4_datadir/autostart

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-4
- set INCLUDE_INSTALL_DIR in %%cmake_kde4

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-3
- actually create the directory listed in the file list

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 4-2
- set kde4_includedir to %%_kde4_prefix/include/kde4

* Mon Nov 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4-1
- Version: 4
- %%cmake_kde4: add -DCMAKE_SKIP_RPATH:BOOL=ON
- Requires: redhat-rpm-config (for proper rpm macro defs)
  (hmm... may need a new -devel pkg somewhere)

* Mon Aug 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-9
- BR: gawk
- - %%_prefix/{env,shutdown} (non-FHS)

* Wed Aug 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-8
- simplify macros a bit

* Tue Aug 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-7
- kde4-macros(api), %%_kde4_macros_api

* Fri Aug 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-6
- restore kde3 dirs

* Thu Aug 09 2007 Than Ngo <than@redhat.com> - 3.92-5
- use macros

* Thu Aug 09 2007 Than Ngo <than@redhat.com> - 3.92-4
- fix kde4 macro

* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92-3
- cleanup macros.kde4 (mostly use _kde4_ prefix)
- Requires: rpm

* Tue Aug 07 2007 Than Ngo <than@redhat.com> 3.92-2
- add missing macros.kde4

* Mon Aug 06 2007 Than Ngo <than@redhat.com> - 3.92-1
- kde4 filesystem
- add KDE4 macros

* Thu Jul 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-9
- +%%_datadir/{sounds,templates/.source,wallpapers}

* Wed Jul 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-8
- +%%_datadir/{autostart,emoticons,mimelnk/*}
- +%%_sysconfdir/kde/xdg

* Wed Jul 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-7
- - %%_datadir/icons (owned by filesystem)
- + %%_datadir/icons/locolor (until owned elsewhere)

* Fri Dec 01 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-6
- + %%_datadir/templates (kdebase,koffice)

* Wed Oct 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-5
- + %%_datadir/icons/locolor

* Tue Oct 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-4
- drop/omit %%_datadir/locale/all_languages

* Fri Oct 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-3
- + %%_datadir/desktop-directories
- + %%_datadir/locale/all_languages

* Thu Oct 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-2
- + %%_datadir/applnk/.hidden
- + %%_sysconfdir/kde/kdm
- + %%docdir/HTML/en

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-1
- first try
