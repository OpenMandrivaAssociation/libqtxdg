%define major 1
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname qt5xdg %{major}
%define devname %mklibname qt5xdg -d

%define qt4libname %mklibname qtxdg %{major}
%define qt4devname %mklibname qtxdg -d

Name: libqtxdg
Version: 1.3.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 2
Source0: https://github.com/lxde/libqtxdg/archive/%{name}-%{version}.tar.xz
%else
Release: 1.%{scmrev}.1
# git clone https://github.com/lxde/libqtxdg.git
# git archive --format=tar --prefix libqtxdg-1.0.0-$(date +%Y%m%d)/ HEAD | xz -vf > libqtxdg-1.0.0-$(date +%Y%m%d).tar.xz
Source0: %{name}-%{version}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 1.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.xz
%else
Release: 1.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Patch100: libqtxdg-1.1.0-use-xvt.patch
Summary: Library providing freedesktop.org specs implementations for Qt
URL: http://lxqt.org/
License: GPL
Group: System/Libraries
Patch8: 0009-XdgDesktopFile-Handles-NotShowIn-correctly.patch
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: ninja
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Xml)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Test)
%rename %{name}-data

%description
Library providing freedesktop.org specs implementations for Qt.

%package -n %{libname}
Summary: Library providing freedesktop.org specs implementations for Qt
Group: System/Libraries
%rename %{qt4libname}

%description -n %{libname}
Library providing freedesktop.org specs implementations for Qt.

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
%setup -q -n %{name}-%{version}-%{scmrev}
%endif
%apply_patches

%cmake_qt5 -G Ninja -DCMAKE_MAKE_PROGRAM=ninja

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja -C build install
# Fix up the pkgconfig file...
sed -i -e 's,\${prefix}/,,g' "%{buildroot}"%{_libdir}/pkgconfig/*.pc

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/qt5xdg
