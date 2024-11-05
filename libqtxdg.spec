%define major 4
#define beta %{nil}
#define scmrev %{nil}
%define libname %mklibname Qt6Xdg
%define devname %mklibname Qt6Xdg -d

#global __requires_exclude ^cmake.*XdgIconLoader.*$

Name: libqtxdg
Version: 4.1.0
Release: %{?beta:0.%{beta}.}%{?scmrev:0.%{scmrev}.}1
Source0: https://github.com/lxqt/libqtxdg/archive/%{version}.tar.gz
Summary: Library providing freedesktop.org specs implementations for Qt
URL: https://lxqt.org/
License: GPL
Group: System/Libraries
Patch100: libqtxdg-1.1.0-use-xvt.patch
BuildRequires: cmake
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(lxqt2-build-tools) >= 0.6.0
BuildRequires: ninja
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Xml)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Svg)
%rename %{name}-data

%description
Library providing freedesktop.org specs implementations for Qt.

%package -n %{libname}
Summary: Library providing freedesktop.org specs implementations for Qt
Group: System/Libraries

%description -n %{libname}
Library providing freedesktop.org specs implementations for Qt.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
Requires: pkgconfig(gio-unix-2.0)

%description -n %{devname}
Development files (Headers etc.) for %{name}, a library providing
freedesktop.org specs implementations for Qt.

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:%{beta}}
%cmake -G Ninja -DCMAKE_MAKE_PROGRAM=ninja

%build
%ninja -C build

%install
%ninja_install -C build

# Fix up the pkgconfig file...
sed -i -e 's,\${prefix}/,,g' "%{buildroot}"%{_libdir}/pkgconfig/*.pc

# We prefer qterminal over xterm even when not using LXQt
sed -i -e 's,xterm,qterminal,g' %{buildroot}%{_sysconfdir}/xdg/qtxdg.conf

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/qt6/plugins/iconengines/libQt6XdgIconPlugin.so
%{_sysconfdir}/xdg/lxqt-qtxdg.conf
%{_sysconfdir}/xdg/qtxdg.conf

%files -n %{devname}
%dir %{_datadir}/cmake/qt6xdg
%dir %{_datadir}/cmake/qt6xdgiconloader
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/qt6xdg/*.cmake
%{_datadir}/cmake/qt6xdgiconloader/*.cmake
