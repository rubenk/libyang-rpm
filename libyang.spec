%global commit 7d0e8648a2f803c149d5e8ab442b8d9ce7f8524a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Name: libyang
Version: 0.16.129
Release: 0
Summary: A YANG parser and toolkit
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
License: BSD

BuildRequires:  cmake
BuildRequires:  libcmocka-devel
BuildRequires:  doxygen
BuildRequires:  pcre-devel
BuildRequires:  gcc


%package devel
Summary:    Headers of libyang library
Requires:   %{name} = %{version}-%{release}
Requires:   pcre-devel

%description devel
Headers of libyang library.


%description
A YANG data modelling language parser and toolkit.


%prep
%autosetup -n %{name}-%{commit}
mkdir build

# spurious executable permissions
chmod -x src/extensions/yangdata.c
chmod -x src/printer_yang.c
chmod -x src/tree_schema.c


%build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
   -DCMAKE_BUILD_TYPE:String="Package" \
   -DENABLE_LYD_PRIV=ON \
   -DGEN_JAVA_BINDINGS=OFF \
   -DGEN_JAVASCRIPT_BINDINGS=OFF \
   -DENABLE_VALGRIND_TESTS=OFF \
   -DGEN_LANGUAGE_BINDINGS=OFF \
   ..

make %{?_smp_mflags}


%check
cd build
ctest --output-on-failure


%install
cd build
make DESTDIR=%{buildroot} install


%ldconfig_scriptlets


%files
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz
%{_libdir}/libyang.so.0.16
%{_libdir}/libyang.so.0.16.129
%{_libdir}/libyang/extensions/metadata.so
%{_libdir}/libyang/extensions/nacm.so
%{_libdir}/libyang/extensions/yangdata.so
%{_libdir}/libyang/user_types/user_date_and_time.so
%dir %{_libdir}/libyang/


%files devel
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/dict.h
%{_includedir}/libyang/extensions.h
%{_includedir}/libyang/libyang.h
%{_includedir}/libyang/tree_data.h
%{_includedir}/libyang/tree_schema.h
%{_includedir}/libyang/user_types.h
%{_includedir}/libyang/xml.h
%dir %{_includedir}/libyang/


%changelog
* Wed Mar 20 2019 Ruben Kerkhof <ruben@tilaa.com> - 0.16.129-0
- Upgrade to 0.16.129

* Thu Feb 21 2019  ci <ci@ci105.lab.netdef.org> 0.16.111-0
- unknown changes
