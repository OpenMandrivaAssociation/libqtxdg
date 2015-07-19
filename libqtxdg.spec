%define major 1
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname qt5xdg %{major}
%define devname %mklibname qt5xdg -d

%define qt4libname %mklibname qtxdg %{major}
%define qt4devname %mklibname qtxdg -d

Name: libqtxdg
Version: 1.2.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 4
Source0: %{name}-%{version}.tar.xz
%else
Release: 0.%{scmrev}.1
# git clone https://github.com/lxde/libqtxdg.git
# git archive --format=tar --prefix libqtxdg-1.0.0-$(date +%Y%m%d)/ HEAD | xz -vf > libqtxdg-1.0.0-$(date +%Y%m%d).tar.xz
Source0: %{name}-%{version}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.xz
%else
Release: 0.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Patch100: libqtxdg-1.1.0-use-xvt.patch
Summary: Library providing freedesktop.org specs implementations for Qt
URL: http://lxqt.org/
License: GPL
Group: System/Libraries
Patch0: 0001-Get-rid-of-Qt4-stuff-in-the-build-system.patch
Patch1: 0002-Remove-Qt4-stuff-from-the-source-files.patch
Patch2: 0003-Remove-Qt4-stuff-from-the-example-and-tests.patch
Patch3: 0004-Remove-Qt4-stuff-from-the-documentation.patch
Patch4: 0005-Cleans-up-empty-comment-lines.patch
Patch5: 0006-Gets-rid-of-translations-stuff.patch
Patch6: 0007-QIconLoader-Change-the-order-fallback-icon-lookup-or.patch
Patch7: 0008-Fixes-XdgDirs-dataHome-regression.patch
Patch8: 0009-XdgDesktopFile-Handles-NotShowIn-correctly.patch
Patch9: 0010-Adds-XdgDirs-configHome-fallback-default-locations.patch
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
