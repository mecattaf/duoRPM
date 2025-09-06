# This is needed for astal-tray functionality
%global commit0 f05d28d805a22a7564895aa178772361c44b6b7a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global _vpath_srcdir subprojects/appmenu-glib-translator

Name:           appmenu-glib-translator
Version:        25.04^1.git%{shortcommit0}
Release:        %autorelease
Summary:        GLib translator for application menus

License:        LGPL-3.0-or-later
URL:            https://github.com/rilian-la-te/vala-panel-appmenu
Source:         %{url}/archive/%{commit0}/vala-panel-appmenu-%{shortcommit0}.tar.gz

BuildRequires:  meson >= 0.59.0
BuildRequires:  gcc
BuildRequires:  vala
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%description
GLib translator for application menus, required for system tray
functionality in Astal.

%prep
%autosetup -n vala-panel-appmenu-%{commit0} -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_libdir}/girepository-1.0/AppmenuGLibTranslator-25.04.typelib
%{_libdir}/libappmenu-glib-translator.so.0
%{_libdir}/libappmenu-glib-translator.so.25.04

%files devel
%{_datadir}/gir-1.0/AppmenuGLibTranslator-25.04.gir
%{_datadir}/vala/vapi/appmenu-glib-translator.deps
%{_datadir}/vala/vapi/appmenu-glib-translator.vapi
%{_includedir}/appmenu-glib-translator/
%{_libdir}/libappmenu-glib-translator.so
%{_libdir}/pkgconfig/appmenu-glib-translator.pc

%changelog
%autochangelog
