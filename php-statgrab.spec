%define modname statgrab
%define soname %{modname}.so
%define inifile A87_%{modname}.ini

Summary:	Libstatgab bindings for PHP
Name:		php-%{modname}
Version:	0.6.0
Release:	21
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/statgrab
Source0:	http://pecl.php.net/get/Statgrab-%{version}.tgz
Patch0:		Statgrab-0.6.0-version_fix.diff
Patch1:		Statgrab-0.6.0-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libstatgrab-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libstatgrab is a library that provides a common interface for retrieving a
variety of system statistics on a number of *NIX like systems.

This extension allows you to call the functions made available by libstatgrab
library.

%prep

%setup -q -n Statgrab-%{version}
[ "../package*.xml" != "/" ] && mv -f ../package*.xml .
%patch0 -p0
%patch1 -p0

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS statgrab.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-20mdv2012.0
+ Revision: 797017
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-19
+ Revision: 761297
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-18
+ Revision: 696472
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-17
+ Revision: 695467
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-16
+ Revision: 646687
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-15mdv2011.0
+ Revision: 629872
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-14mdv2011.0
+ Revision: 628192
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-13mdv2011.0
+ Revision: 600532
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-12mdv2011.0
+ Revision: 588870
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-11mdv2010.1
+ Revision: 514659
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-10mdv2010.1
+ Revision: 485485
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-9mdv2010.1
+ Revision: 468256
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-8mdv2010.0
+ Revision: 451359
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.6.0-7mdv2010.0
+ Revision: 397606
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-6mdv2010.0
+ Revision: 377029
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-5mdv2009.1
+ Revision: 346636
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-4mdv2009.1
+ Revision: 341801
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-3mdv2009.1
+ Revision: 323089
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-2mdv2009.1
+ Revision: 310309
- rebuilt against php-5.2.7

* Fri Nov 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-1mdv2009.1
+ Revision: 305480
- import php-statgrab


* Fri Nov 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-1mdv2009.0
- initial Mandriva package
