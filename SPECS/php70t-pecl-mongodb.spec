%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name mongodb
%global real_name php-pecl-mongodb
%global basever 1
%global php_base php70t
%global date 20151222

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


Summary:      PHP MongoDB database driver
Name:         %{php_base}-pecl-mongodb
Version:      1.1.0
Release:      2.%{?date}.vortex%{?dist}
License:      ASL 2.0
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: %{php_base}-devel, %{php_base}-pear, openssl-devel, cyrus-sasl-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if 0%{?php_zend_api:1}
Requires:     %{php_base}(zend-abi) = %{php_zend_api}
Requires:     %{php_base}(api) = %{php_core_api}
%else
Requires:     %{php_base}-api = %{php_apiver}
%endif
Provides:     %{real_name} = %{version}-%{release}
Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     %{php_base}-pecl(%{pecl_name}) = %{version}-%{release}


%description
This package provides an interface for communicating with the MongoDB database
in PHP.

%prep
%setup -c -q
cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

;  option documentation: http://www.php.net/manual/en/mongo.configuration.php

;  If persistent connections are allowed.
;mongo.allow_persistent = 1

;  Whether to reconnect to the database if the connection is lost.
;mongo.auto_reconnect = 1

;  The number of bytes-per-chunk.
;  This number must be at least 100 less than 4 megabytes (max: 4194204)
;mongo.chunk_size = 262144

;  A character to be used in place of $ in modifiers and comparisons.
;mongo.cmd = $

;  Default hostname when nothing is passed to the constructor.
;mongo.default_host = localhost

;  The default TCP port number. The database's default is 27017.
;mongo.default_port = 27017

;  Return a BSON_LONG as an instance of MongoInt64
;  (instead of a primitive type).
;mongo.long_as_object = 0

;  Use MongoDB native long (this will default to true for 1.1.0)
mongo.native_long = true

;  If an exception should be thrown for non-UTF8 strings.
;  This option will be eliminated and exceptions always thrown for non-UTF8
;  strings starting with version 1.1.0.
mongo.utf8 = 1
EOF

# Install XML package description
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/README.md
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Tue Dec 22 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.1.0-2.20151222.vortex
- Git sources.

* Fri Dec 18 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.1.0-1.vortex
- Update to 1.1.0.

* Sat Dec 12 2015 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.0.1-1.vortex
- Initial packaging.
