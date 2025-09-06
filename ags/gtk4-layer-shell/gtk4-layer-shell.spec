Name:           gtk4-layer-shell
Version:        1.2.0
Release:        1%{?dist}
Summary:        Library to create panels and other desktop components for Wayland

License:        MIT
URL:            https://github.com/wmww/gtk4-layer-shell
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.45.1
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(wayland-client) >= 1.10.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.16
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala

%description
A library for using the Layer Shell Wayland protocol with GTK4. With this
library you can build desktop panels, launchers, and other such overlays.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%prep
%autosetup -p1

%build
%meson \
    -Dexamples=false \
    -Ddocs=false \
    -Dtests=false
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libgtk4-layer-shell.so.0*
%{_libdir}/girepository-1.0/Gtk4LayerShell-1.0.typelib

%files devel
%{_includedir}/gtk4-layer-shell/
%{_libdir}/libgtk4-layer-shell.so
%{_libdir}/pkgconfig/gtk4-layer-shell-0.pc
%{_datadir}/gir-1.0/Gtk4LayerShell-1.0.gir
%{_datadir}/vala/vapi/gtk4-layer-shell-0.deps
%{_datadir}/vala/vapi/gtk4-layer-shell-0.vapi

%changelog
* %{DATE} Thomas Mecattaf <thomas@mecattaf.dev> - 1.2.0-1
- Update to 1.2.0
- Support for GTK 4.16
- Improved Wayland protocol compliance
