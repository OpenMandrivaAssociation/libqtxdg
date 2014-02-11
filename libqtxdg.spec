%define major 0
%define beta %{nil}
%define scmrev 20140211
%define libname %mklibname qtxdg %{major}
%define devname %mklibname qtxdg -d

Name: libqtxdg
Version: 0.1
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 1
Source: %{name}-%{version}.tar.bz2
%else
Release: 0.%{scmrev}.1
Source: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.%{scmrev}.1
Source: %{name}-%{scmrev}.tar.xz
%endif
%endif
Summary: Library providing freedesktop.org specs implementations for Qt
URL: http://lxde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt4-devel
BuildRequires: magic-devel
Requires: %{libname} = %{EVRD}

%description
Library providing freedesktop.org specs implementations for Qt

%package -n %{libname}
Summary: Library providing freedesktop.org specs implementations for Qt
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Library providing freedesktop.org specs implementations for Qt

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}, a library providing
freedesktop.org specs implementations for Qt.

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}
%endif
%cmake -G Ninja -DCMAKE_MAKE_PROGRAM=ninja

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja -C build install
# Fix up the pkgconfig file...
sed -i -e 's,\${prefix}/,,g' "%{buildroot}"%{_libdir}/pkgconfig/*.pc

%files
%dir %{_datadir}/libqtxdg
%{expand:%(for lang in ar cs cs_CZ da da_DK de_DE el_GR eo es es_VE eu fi fr_FR hu id_ID it_IT ja lt nl pl_PL pt pt_BR ro_RO ru ru_RU sk_SK sl sr_RS th_TH tr uk zh_CN zh_TW; do echo %{_datadir}/libqtxdg/libqtxdg_$lang.qm; done)}

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/qtxdg
