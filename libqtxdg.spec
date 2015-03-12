%define major 1
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname qt5xdg %{major}
%define devname %mklibname qt5xdg -d

%define qt4libname %mklibname qtxdg %{major}
%define qt4devname %mklibname qtxdg -d

Name: libqtxdg
Version: 1.1.0
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
Patch0: 0001-QIconLoader-remove-an-unused-variable.patch
Patch1: 0002-QIconLoader-remove-another-unused-variable.patch
Patch2: 0003-QIconLoader-don-t-re-evaluate-container.size-all-the.patch
Patch3: 0004-QIconLoader-don-t-re-evaluate-container.size-all-the.patch
Patch4: 0005-QIconLoader-replace-while-empty-delete-takeLast-with.patch
Patch5: 0006-QIconLoader-mark-a-helper-type-as-movable.patch
Patch6: 0007-QIconLoader-mark-virtual-overrides.patch
Patch7: 0008-QIconLoader-replace-an-inefficient-QList-with-a-QVec.patch
Patch8: 0009-QIconLoader-don-t-inherit-QObject.patch
Patch9: 0010-QIconLoader-enable-an-easy-case-of-transactional-pro.patch
Patch10: 0011-Use-QPlatformTheme-SystemIconFallbackThemeName-in-st.patch
Patch11: 0012-Update-license-headers-and-add-new-license-files.patch
Patch12: 0013-Avoid-adding-empty-parent-icon-theme.patch
Patch13: 0014-Release-with-a-proper-versioned-prefix.patch
Patch14: 0015-Fix-compilation-when-using-internal-mime.patch
Patch15: 0016-Makes-needed-helper-functions-available-to-tests.patch
Patch16: 0017-Ignore-empty-dirs-in-xdgDirList.patch
Patch17: 0018-Qt5-Use-Qt5-private-headers.patch
Patch18: 0019-Quote-all-paths-in-the-CMake-stuff.patch
Patch19: 0020-XdgDesktopFileCache-Retrieve-apps-of-a-category.patch
Patch20: 0021-Replace-empty-quotes-by-QString.patch
Patch21: 0022-Fix-XdgDirs-dataDirs-postfix-handling.patch
Patch22: 0023-XdgDirs-configHome-handle-postfix-slash.patch
Patch23: 0024-XdgDirs-postfix-should-always-start-with-an.patch
Patch24: 0025-Make-sure-returned-directories-don-t-have-an-trailin.patch
Patch26: 0026-String-manipulation-enhancements.patch
Patch27: 0027-XdgDirs-Updates-documentation.patch
Summary: Library providing freedesktop.org specs implementations for Qt
URL: http://lxqt.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: ninja
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Xml)
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
