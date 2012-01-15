%define modname statgrab
%define soname %{modname}.so
%define inifile A87_%{modname}.ini

Summary:	Libstatgab bindings for PHP
Name:		php-%{modname}
Version:	0.6.0
Release:	%mkrel 19
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/statgrab
Source0:	http://pecl.php.net/get/Statgrab-%{version}.tgz
Patch0:		Statgrab-0.6.0-version_fix.diff
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

