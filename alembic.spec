%define major     %(echo %{version}|cut -d. -f1-2)
%define libname   %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:           alembic
Version:	1.8.4
Release:	2
Summary:        Open framework for storing and sharing scene data
License:        BSD
Group:          System/Libraries
URL:            http://alembic.io/
Source0:        https://github.com/%{name}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		alembic-1.8.3-no-openexr2-dep.patch
BuildRequires:  cmake
BuildRequires:  hdf5-devel
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(zlib)
BuildRequires:	ilmbase-devel

%description
Alembic is an open computer graphics interchange framework. Alembic distills
complex, animated scenes into a non-procedural, application-independent set of
baked geometric results. This 'distillation' of scenes into baked geometry is
exactly analogous to the distillation of lighting and rendering scenes into
rendered image data.

#------------------------------------------------

%package -n     %{libname}
Summary:        Open framework for storing and sharing scene data
Group:          System/Libraries

%description -n %{libname}
Alembic is an open computer graphics interchange framework. Alembic distills
complex, animated scenes into a non-procedural, application-independent set of
baked geometric results. This 'distillation' of scenes into baked geometry is
exactly analogous to the distillation of lighting and rendering scenes into
rendered image data.

#------------------------------------------------

%package -n     %{develname}
Summary:        Development files for %{name}
Group:          Development/C++
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
The %{develname} package contains libraries and header files for developing
applications that use %{name}.

#------------------------------------------------

%prep
%autosetup -p1

# Hardcoded library path
sed -i -e 's/INSTALL_DIR lib/INSTALL_DIR %{_lib}/g' CMakeLists.txt
sed -i \
    -e 's/INSTALL_DIR lib/INSTALL_DIR %{_lib}/g' \
    -e 's/ConfigPackageLocation lib/ConfigPackageLocation %{_lib}/g' \
    lib/Alembic/CMakeLists.txt

iconv -f iso8859-1 -t utf-8 ACKNOWLEDGEMENTS.txt > ACKNOWLEDGEMENTS.txt.conv && \
    mv -f ACKNOWLEDGEMENTS.txt.conv ACKNOWLEDGEMENTS.txt

%build
%cmake \
    -DALEMBIC_SHARED_LIBS=ON \
    -DUSE_BINARIES=ON \
    -DUSE_HDF5=ON \
    -DUSE_EXAMPLES=ON \
    -DUSE_PYALEMBIC=OFF \
    -DUSE_STATIC_BOOST=OFF \
    -DUSE_STATIC_HDF5=OFF \
    -DUSE_TESTS=ON

%make_build

%install
%make_install -C build

%files
%doc ACKNOWLEDGEMENTS.txt FEEDBACK.txt NEWS.txt README.txt
%license LICENSE.txt
%{_bindir}/abcconvert
%{_bindir}/abcdiff
%{_bindir}/abcecho
%{_bindir}/abcechobounds
%{_bindir}/abcls
%{_bindir}/abcstitcher
%{_bindir}/abctree

%files -n %{libname}
%{_libdir}/libAlembic.so.%{major}{,.*}

%files -n %{develname}
%{_includedir}/Alembic/
%{_libdir}/cmake/Alembic/
%{_libdir}/libAlembic.so
