%define major 4
#define beta %{nil}
#define scmrev %{nil}
%define libname %mklibname Qt6Xdg
%define devname %mklibname Qt6Xdg -d

Name:		libqtxdg
Version:	4.4.0
Release:	%{?beta:0.%{beta}.}%{?scmrev:0.%{scmrev}.}3
Source0:	https://github.com/lxqt/libqtxdg/releases/download/%{version}/libqtxdg-%{version}.tar.xz
Summary:	Library providing freedesktop.org specs implementations for Qt
URL:		https://lxqt-project.org/
License:	LGPL-2.1+
Group:		System/Libraries
BuildSystem:	cmake
BuildRequires:	cmake(lxqt2-build-tools) >= 2.4.0
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6GuiPrivate)
%rename %{name}-data

%patchlist
libqtxdg-1.1.0-use-xvt.patch

%description
Library providing freedesktop.org specs implementations for Qt.

%package -n %{libname}
Summary:	Library providing freedesktop.org specs implementations for Qt
Group:		System/Libraries

%description -n %{libname}
Library providing freedesktop.org specs implementations for Qt.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}, a library providing
freedesktop.org specs implementations for Qt.

%install -a
# Make sure the "uncommon" dependency is found
sed -i -e '/CMAKE_IMPORT_FILE_VERSION 1/ifind_package(Qt6 "6.0.0" REQUIRED COMPONENTS GuiPrivate)' %{buildroot}%{_datadir}/cmake/qt6xdgiconloader/qt6xdgiconloader-targets.cmake

%files -n %{libname}
%license COPYING
%{_libdir}/*.so.%{major}*
%{_libdir}/qt6/plugins/iconengines/libQt6XdgIconPlugin.so
%config(noreplace) %{_sysconfdir}/xdg/lxqt-qtxdg.conf
%config(noreplace) %{_sysconfdir}/xdg/qtxdg.conf

%files -n %{devname}
%dir %{_datadir}/cmake/qt6xdg
%dir %{_datadir}/cmake/qt6xdgiconloader
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/qt6xdg/*.cmake
%{_datadir}/cmake/qt6xdgiconloader/*.cmake
