%define major 3
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname qt5xdg
%define oldlibname %mklibname qt5xdg 3
%define devname %mklibname qt5xdg -d

%define qt4libname %mklibname qtxdg %{major}
%define qt4devname %mklibname qtxdg -d

%global __requires_exclude ^cmake.*XdgIconLoader.*$

Name: libqtxdg
Version: 3.10.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 2
Source0: https://github.com/lxqt/libqtxdg/archive/%{version}.tar.gz
%else
Release: 2
# git clone https://github.com/lxde/libqtxdg.git
# git archive --format=tar --prefix libqtxdg-1.0.0-$(date +%Y%m%d)/ HEAD | xz -vf > libqtxdg-1.0.0-$(date +%Y%m%d).tar.xz
Source0: %{name}-%{version}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 2
Source0: %{name}-%{version}%{beta}.tar.xz
%else
Release: 2
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Summary: Library providing freedesktop.org specs implementations for Qt
URL: http://lxqt.org/
License: GPL
Group: System/Libraries
Patch100: libqtxdg-1.1.0-use-xvt.patch
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(lxqt-build-tools) >= 0.6.0
BuildRequires: ninja
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Xml)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5Svg)
%rename %{name}-data

%description
Library providing freedesktop.org specs implementations for Qt.

%package -n %{libname}
Summary: Library providing freedesktop.org specs implementations for Qt
Group: System/Libraries
%rename %{qt4libname}
%rename %{oldlibname}

%description -n %{libname}
Library providing freedesktop.org specs implementations for Qt.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
%rename %{qt4devname}
Requires: pkgconfig(gio-unix-2.0)

%description -n %{devname}
Development files (Headers etc.) for %{name}, a library providing
freedesktop.org specs implementations for Qt.

%prep
%if "%{scmrev}" == ""
%autosetup -p1 -n %{name}-%{version}%{beta}
%else
%autosetup -p1 -n %{name}-%{version}-%{scmrev}
%endif

%cmake_qt5 -G Ninja -DCMAKE_MAKE_PROGRAM=ninja

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
%{_libdir}/qt5/plugins/iconengines/libQt5XdgIconPlugin.so
%{_sysconfdir}/xdg/lxqt-qtxdg.conf
%{_sysconfdir}/xdg/qtxdg.conf

%files -n %{devname}
%dir %{_datadir}/cmake/qt5xdg
%dir %{_datadir}/cmake/qt5xdgiconloader
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/qt5xdg/*.cmake
%{_datadir}/cmake/qt5xdgiconloader/*.cmake
