Name:           gray
Version:        0.1.0
Release:        1%{?dist}
Summary:        System trays for everyone - SNI protocol implementation library

License:        AGPL-3.0-or-later
URL:            https://github.com/Fabric-Development/gray
# Use git snapshot since no releases exist yet
%global commit          main
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(dbusmenu-glib-0.4)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

# For typelib generation
BuildRequires:  gobject-introspection-devel

Requires:       gtk3
Requires:       libdbusmenu-gtk3
Requires:       glib2

%description
Gray is an implementation of the SNI (Status Notifier Item) protocol that makes
creating system trays super simple. It provides GObject introspection bindings
for multiple programming languages including Python, JavaScript (GJS), Lua,
Vala, and C.

Features:
- Complete SNI protocol implementation
- GObject introspection support for multiple languages
- Simple API for creating system tray widgets
- Support for icon pixmaps and theme icons
- Context menu integration via DBusMenu
- Tooltip support

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gtk3-devel
Requires:       libdbusmenu-gtk3-devel
Requires:       glib2-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{name}-%{commit}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libgray.so.*
%{_libdir}/girepository-1.0/Gray-0.1.typelib

%files devel
%doc examples/
%{_includedir}/libgray.h
%{_libdir}/libgray.so
%{_libdir}/pkgconfig/gray.pc
%{_datadir}/gir-1.0/Gray-0.1.gir
%{_datadir}/vala/vapi/Gray-0.1.vapi

%changelog
* Sun Jul 20 2025 Package Maintainer <maintainer@example.com> - 0.1.0-1
- Initial package for Gray SNI implementation library using git snapshot
%autochangelog
