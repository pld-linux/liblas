#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	gdal		# GDAL support
%bcond_without	laszip		# LASzip support
#
Summary:	LAS 1.0/1.1/1.2 ASPRS LiDAR data translation toolset
Summary(pl.UTF-8):	Narzędzia do tłumaczenia danych LiDARowych ASPRS LAS 1.0/1.1/1.2
Name:		liblas
Version:	1.8.1
Release:	9
License:	BSD with Boost v1.0 and MIT parts
Group:		Libraries
Source0:	http://download.osgeo.org/liblas/libLAS-%{version}.tar.bz2
# Source0-md5:	2e6a975dafdf57f59a385ccb87eb5919
# https://github.com/libLAS/libLAS/pull/166.patch
Patch0:		%{name}-boost-endian.patch
# from Fedora, modified
Patch1:		%{name}-boost1.73.patch
# https://github.com/libLAS/libLAS/issues/164
Patch2:		%{name}-gdal3.patch
# https://github.com/libLAS/libLAS/issues/159
Patch3:		%{name}-CVE-2018-20539.patch
# https://github.com/libLAS/libLAS/issues/161
Patch4:		%{name}-CVE-2018-20536.patch
# https://github.com/libLAS/libLAS/issues/160
Patch5:		%{name}-CVE-2018-20537.patch
# https://github.com/libLAS/libLAS/issues/181, modified
Patch6:		%{name}-CVE-2018-20540.patch
Patch7:		%{name}-pkgconfig.patch
Patch8:		%{name}-cxxstd.patch
Patch9:		gcc14.patch
Patch10:	intersphinx.patch
URL:		https://liblas.org/
BuildRequires:	boost-devel >= 1.38
BuildRequires:	cmake >= 2.6.0
%{?with_gdal:BuildRequires:	gdal-devel >= 1.7.0}
%{?with_laszip:BuildRequires:	laszip-devel >= 2.0.1}
BuildRequires:	libgeotiff-devel >= 1.3.0
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
%{?with_gdal:BuildRequires:	proj-devel >= 4}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-rst2pdf
BuildRequires:	sphinx-pdg-3
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libLAS is a C/C++ library for reading and writing the very common LAS
LiDAR format. The ASPRS LAS format is a sequential binary file format
used to store data from LiDAR sensors and by LiDAR processing software
for data interchange and archival.

%description -l pl.UTF-8
libLAS to biblioteka C/C++ do odczytu i zapisu popularnego formatu
danych LiDARowych LAS. Format ASPRS LAS to sekwencyjny format plików
binarnych używany do zapisu danych z czujników LiDARowych oraz
oprogoramowania przetwarzającego dane LiDARowe na potrzeby wymiany i
archiwizacji.

%package devel
Summary:	Header files for libLAS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libLAS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_gdal:Requires:	gdal-devel >= 1.7.0}
Requires:	libgeotiff-devel >= 1.3.0
Requires:	libstdc++-devel

%description devel
Header files for libLAS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libLAS.

%package apidocs
Summary:	API documentation for libLAS library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libLAS
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libLAS library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libLAS.

%prep
%setup -q -n libLAS-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1
%patch -P 9 -p1
%patch -P 10 -p1

%build
install -d build
cd build
%cmake .. \
	-DLIBLAS_LIB_SUBDIR=%{_lib} \
	%{?with_gdal:-DWITH_GDAL=ON} \
	%{?with_laszip:-DWITH_LASZIP=ON} \
	-DWITH_PKGCONFIG=ON

%{__make}
cd ..

%if %{with apidocs}
cd doc
LD_LIBRARY_PATH=$(pwd)/../build/bin/PLD sphinx-build-3 -b html . _build/html
cd api
doxygen doxygen.conf
%{__mv} html ../_build/html/api
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc or dummy
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/liblas/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE.txt
%attr(755,root,root) %{_bindir}/las2col
%attr(755,root,root) %{_bindir}/las2las
%if %{with gdal}
%attr(755,root,root) %{_bindir}/las2ogr
%endif
%attr(755,root,root) %{_bindir}/las2pg
%attr(755,root,root) %{_bindir}/las2txt
%attr(755,root,root) %{_bindir}/lasblock
%attr(755,root,root) %{_bindir}/lasinfo
%attr(755,root,root) %{_bindir}/ts2las
%attr(755,root,root) %{_bindir}/txt2las
%attr(755,root,root) %{_libdir}/liblas.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblas.so.3
%attr(755,root,root) %{_libdir}/liblas_c.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblas_c.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblas.so
%attr(755,root,root) %{_libdir}/liblas_c.so
%{_includedir}/liblas
%{_pkgconfigdir}/liblas.pc
%{_datadir}/cmake/libLAS

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,api,development,tutorial,utilities,*.html,*.js}
%endif
