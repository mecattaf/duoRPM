# ========================================
# astal-gtk4.spec - GTK4 variant (Vala/C)
# ========================================
%global astal_commit 20bd8318e4136fbd3d4eb2d64dbabc3acbc915dd
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 1

# Bootstrap conditional
%bcond bootstrap 0

%global _vpath_srcdir lib/astal/gtk4

Name:           astal-gtk4
Version:        4.0.0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Building blocks for creating custom desktop shells with GTK4

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/astal-%{astal_shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.59.0
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
# No longer requires astal-io

Requires:       gtk4-layer-shell%{?_isa} >= 1.2.0
# Remove version lock to avoid circular deps
Requires:       astal%{?_isa}

%if %{without bootstrap}
Requires:       astal-libs%{?_isa}
%endif

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%description
Astal GTK4 provides the GTK4 variant of the Astal library for building
custom desktop shells and widgets for Wayland compositors. Written in Vala/C.

%prep
%autosetup -n astal-%{astal_commit} -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_libdir}/girepository-1.0/Astal-4.0.typelib
%{_libdir}/libastal-4.so.4*

%files devel
%{_datadir}/gir-1.0/Astal-4.0.gir
%{_datadir}/vala/vapi/astal-4-4.0.vapi
%{_includedir}/astal-4.h
%{_libdir}/libastal-4.so
%{_libdir}/pkgconfig/astal-4-4.0.pc

%changelog
%autochangelog
