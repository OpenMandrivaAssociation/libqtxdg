%define major 1
%define beta %{nil}
%define scmrev 20141017
%define libname %mklibname qt5xdg %{major}
%define devname %mklibname qt5xdg -d

%define qt4libname %mklibname qtxdg %{major}
%define qt4devname %mklibname qtxdg -d

Name: libqtxdg
Version: 1.0.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 1
Source0: %{name}-%{version}.tar.bz2
%else
Release: 0.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Summary: Library providing freedesktop.org specs implementations for Qt
URL: http://lxde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: ninja
BuildRequires: qt5-devel
BuildRequires: magic-devel

%description
Library providing freedesktop.org specs implementations for Qt

%package data
Summary: Data files for %{name}
Group: System/Libraries
Requires: %{libname} = %{EVRD}

%description data
Data files for %{name}

%package -n %{libname}
Summary: Library providing freedesktop.org specs implementations for Qt
Group: System/Libraries
Requires: %{name}-data = %{EVRD}
%rename %{qt4libname}

%description -n %{libname}
Library providing freedesktop.org specs implementations for Qt

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
%rename %{qt4devname}

%description -n %{devname}
Development files (Headers etc.) for %{name}, a library providing
freedesktop.org specs implementations for Qt.

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}-%{scmrev}
%endif
%cmake -G Ninja -DUSE_QT5=ON -DCMAKE_MAKE_PROGRAM=ninja

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja -C build install
# Fix up the pkgconfig file...
sed -i -e 's,\${prefix}/,,g' "%{buildroot}"%{_libdir}/pkgconfig/*.pc

%files data
%dir %{_datadir}/libqt5xdg
%{expand:%(for lang in ar cs cs_CZ da da_DK de_DE el_GR eo es es_VE eu fi fr_FR hu id_ID it_IT ja lt nl pl_PL pt pt_BR ro_RO ru ru_RU sk_SK sl sr_RS th_TH tr uk zh_CN zh_TW; do echo %{_datadir}/libqt5xdg/libqtxdg_$lang.qm; done)}

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/qt5xdg
