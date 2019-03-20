Name: libyang
Version: 0.16.111
Release: 0
Summary: Libyang library
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/master.tar.gz
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
Libyang is YANG data modelling language parser and toolkit written (and providing API) in C.

%prep
%setup -q -n libyang-master
mkdir build

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

%files
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz
%{_libdir}/libyang.so.*
%{_libdir}/libyang/*
%dir %{_libdir}/libyang/

%files devel
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/*.h
%dir %{_includedir}/libyang/

%changelog
* Thu Feb 21 2019  ci <ci@ci105.lab.netdef.org> 0.16.111-0
- unknown changes
