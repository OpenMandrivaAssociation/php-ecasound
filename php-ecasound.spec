%define realname Ecasound
%define modname ecasound
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A11_%{modname}.ini

Summary:	%{realname} provides audio recording and processing functions for PHP
Name:		php-%{modname}
Version:	0.2
Release:	%mkrel 34
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/ecasound
Source0:	%{realname}-%{version}.tar.bz2
Source1:	%{modname}.ini
Patch0:		Ecasound-0.2-php54x.diff
Requires:	php-cli >= 3:5.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libecasound-devel
Requires:	ecasound
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension wraps the Ecasound libraries to provide advanced audio
processing capabilities.

%prep

%setup -q -n %{realname}-%{version}

%patch0 -p0

cp %{SOURCE1} %{inifile}

%build

%{_usrsrc}/php-devel/buildext %{modname} "%{modname}.c" \
    "-lecasoundc" "-DCOMPILE_DL_ECASOUND -I%{_includedir}/libecasoundc"

#phpize
#%%configure2_5x \
#    --with-%{modname}=shared,%{_prefix}
#
#%%make
#mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc CREDITS ECASOUND_HOWTO README* ecasound.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
