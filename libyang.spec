Name: libyang
Version: 0.16.111
Release: 0
Summary: Libyang library
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/master.tar.gz
License: BSD-3-Clause

%if (0%{?rhel} && 0%{?rhel} < 8) || (0%{?fedora} && 0%{?fedora} < 27)
    %define with_lang_bind 0
%else
    %define with_lang_bind 1
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
    # CentOS/RedHat before 7.0 contains old pcre without pcre_free_study().
    # With cache disabled, this isn't needed
    %define with_enable_cache 0
    # CentOS/RedHat before 7.0 contains old valgrind which can't run
    # valgrind tests. Disable them
    %define with_valgrind 0
%else
    %define with_enable_cache 1
    %define with_valgrind 1
%endif

Requires:  pcre
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  pcre-devel
BuildRequires:  gcc

%if %{with_valgrind}
BuildRequires:  valgrind
%endif

%if %{with_lang_bind}
BuildRequires:  gcc-c++
BuildRequires:  swig >= 3.0.12
BuildRequires:  libcmocka-devel

%if 0%{?suse_version} + 0%{?fedora} > 0
BuildRequires:  python3-devel
%else
BuildRequires:  python34-devel
%endif
%endif

Conflicts: libyang-experimental = 0.16

%package devel
Summary:    Headers of libyang library
Requires:   %{name} = %{version}-%{release}
Requires:   pcre-devel

%if %{with_lang_bind}
%package -n libyang-cpp
Summary:    Bindings to c++ language
Requires:   %{name} = %{version}-%{release}

%package -n libyang-cpp-devel
Summary:    Headers of bindings to c++ language
Requires:   libyang-cpp = %{version}-%{release}
Requires:   pcre-devel

%package -n python3-yang
Summary:    Binding to python
Requires:   libyang-cpp = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

%description -n libyang-cpp
Bindings of libyang library to C++ language.

%description -n libyang-cpp-devel
Headers of bindings to c++ language.

%description -n python3-yang
Bindings of libyang library to python language.
%endif

%description devel
Headers of libyang library.

%description
Libyang is YANG data modelling language parser and toolkit written (and providing API) in C.

%prep
%setup -q -n libyang-master
mkdir build

%build
cd build
%if %{with_lang_bind}
    %define cmake_lang_bind "-DGEN_LANGUAGE_BINDINGS=ON"
%else
    %define cmake_lang_bind "-DGEN_LANGUAGE_BINDINGS=OFF"
%endif
%if %{with_enable_cache}
    %define cmake_enable_cache ""
%else
    %define cmake_enable_cache "-DENABLE_CACHE=OFF"
%endif
%if %{with_valgrind}
    %define cmake_valgrind ""
%else
    %define cmake_valgrind "-DENABLE_VALGRIND_TESTS=OFF"
%endif
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
   -DCMAKE_BUILD_TYPE:String="Package" \
   -DENABLE_LYD_PRIV=ON \
   -DGEN_JAVA_BINDINGS=OFF \
   -DGEN_JAVASCRIPT_BINDINGS=OFF \
   %{cmake_valgrind} %{cmake_lang_bind} %{cmake_enable_cache} ..
make

%check
cd build
ctest --output-on-failure

%install
cd build
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%if %{with_lang_bind}
    %post -n libyang-cpp -p /sbin/ldconfig
%endif

%postun -p /sbin/ldconfig
%if %{with_lang_bind}
    %postun -n libyang-cpp -p /sbin/ldconfig
%endif

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

%if %{with_lang_bind}
%files -n libyang-cpp
%{_libdir}/libyang-cpp.so.*

%files -n libyang-cpp-devel
%{_libdir}/libyang-cpp.so
%{_includedir}/libyang/*.hpp
%{_libdir}/pkgconfig/libyang-cpp.pc
%dir %{_includedir}/libyang/

%files -n python3-yang
%{_libdir}/python*
%endif

%changelog
* Thu Feb 21 2019  ci <ci@ci105.lab.netdef.org> 0.16.111
- unknown changes
