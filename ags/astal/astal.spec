# ========================================
# astal.spec - Main GTK3 library (Vala/C)
# ========================================
%global astal_commit 20bd8318e4136fbd3d4eb2d64dbabc3acbc915dd
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 1

# Bootstrap conditional to handle circular dependencies
%bcond bootstrap 0

%global _vpath_srcdir lib/astal/gtk3

Name:           astal
Version:        3.0.0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Building blocks for creating custom desktop shells with GTK3

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/astal-%{astal_shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.59.0
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)

# No longer requires astal-io (deprecated and merged)

# Bootstrap conditional for circular dependencies
%if %{without bootstrap}
Requires:       astal-libs%{?_isa}
%endif

# Provides for packages that may still reference astal-io
Provides:       astal-io = %{version}-%{release}
Obsoletes:      astal-io < %{version}-%{release}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Provide astal-io-devel for compatibility
Provides:       astal-io-devel = %{version}-%{release}
Obsoletes:      astal-io-devel < %{version}-%{release}

%description    devel
Development files for %{name}.

%description
Astal provides the core GTK3 library for building custom desktop shells
and widgets for Wayland compositors. Written in Vala/C.
Note: astal-io functionality has been merged into this package.

%prep
%autosetup -n astal-%{astal_commit} -p1

%build
# Build both the main library and the io components (if still separate)
%meson
%meson_build

%install
%meson_install

# If astal binary exists from old io module, include it
if [ -f %{buildroot}%{_bindir}/astal ]; then
    echo "Including astal binary"
fi

%files
%license LICENSE
# Main library files
%{_libdir}/girepository-1.0/Astal-3.0.typelib
%{_libdir}/libastal.so.3*
# Include the astal binary if it exists
%{_bindir}/astal
# If AstalIO typelib still exists for compatibility
%{_libdir}/girepository-1.0/AstalIO-0.1.typelib || true

%files devel
%{_datadir}/gir-1.0/Astal-3.0.gir
%{_datadir}/vala/vapi/astal-3.0.vapi
%{_includedir}/astal.h
%{_libdir}/libastal.so
%{_libdir}/pkgconfig/astal-3.0.pc
# Compatibility for old astal-io references
%{_datadir}/gir-1.0/AstalIO-0.1.gir || true
%{_datadir}/vala/vapi/astal-io-0.1.vapi || true
%{_libdir}/pkgconfig/astal-io-0.1.pc || true

%changelog
%autochangelog
