%global astal_commit 344a6dce56437a190b99e516a6cab8332cccf19e
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 2

# Bootstrap conditional to handle circular dependencies
%bcond bootstrap 0

%global _vpath_srcdir lib/astal/io

Name:           astal
Version:        0.1.0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Core library for building custom desktop shells

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/astal-%{astal_shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.59.0
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  python3
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

# Bootstrap conditional for circular dependencies
%if %{without bootstrap}
Requires:       astal-libs%{?_isa}
%endif

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%description
Astal provides the core library for building custom desktop shells
and widgets for Wayland compositors. Written in Vala/C.

%prep
%autosetup -n astal-%{astal_commit} -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
# Core library files
%{_bindir}/astal
%{_libdir}/girepository-1.0/AstalIO-0.1.typelib
%{_libdir}/libastal-io.so.0*

%files devel
%{_datadir}/gir-1.0/AstalIO-0.1.gir
%{_datadir}/vala/vapi/astal-io-0.1.deps
%{_datadir}/vala/vapi/astal-io-0.1.vapi
%{_includedir}/astal-io.h
%{_libdir}/libastal-io.so
%{_libdir}/pkgconfig/astal-io-0.1.pc

%changelog
%autochangelog
