Name:           wayland
Version:        1.23.1
Release:        1%{?dist}
Summary:        Wayland Compositor Infrastructure

# SPDX
License:        MIT
URL:            http://wayland.freedesktop.org/
Source0:        https://gitlab.freedesktop.org/%{name}/%{name}/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  graphviz
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  pkgconfig(libffi)
BuildRequires:  xmlto

%description
Wayland is a protocol for a compositor to talk to its clients as well as a C
library implementation of that protocol. The compositor can be a standalone
display server running on Linux kernel modesetting and evdev input devices,
an X application, or a wayland client itself. The clients can be traditional
applications, X servers (rootless or fullscreen) or other display servers.

%package        devel
Summary:        Development files for %{name}
Requires:       libwayland-client%{?_isa} = %{version}-%{release}
Requires:       libwayland-cursor%{?_isa} = %{version}-%{release}
Requires:       libwayland-egl%{?_isa} = %{version}-%{release}
Requires:       libwayland-server%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Wayland development documentation
BuildArch: noarch
%description doc
Wayland development documentation

%package -n libwayland-client
Summary: Wayland client library
%description -n libwayland-client
Wayland client library

%package -n libwayland-cursor
Summary: Wayland cursor library
Requires: libwayland-client%{?_isa} = %{version}-%{release}
%description -n libwayland-cursor
Wayland cursor library

%package -n libwayland-egl
Summary: Wayland egl library
%description -n libwayland-egl
Wayland egl library

%package -n libwayland-server
Summary: Wayland server library
%description -n libwayland-server
Wayland server library

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files devel
%{_bindir}/wayland-scanner
%{_includedir}/wayland-*.h
%{_libdir}/pkgconfig/wayland-*.pc
%{_libdir}/libwayland-*.so
%{_datadir}/aclocal/wayland-scanner.m4
%dir %{_datadir}/wayland
%{_datadir}/wayland/wayland-scanner.mk
%{_datadir}/wayland/wayland.xml
%{_datadir}/wayland/wayland.dtd
%{_mandir}/man3/*.3*

%files doc
%doc README.md
%{_datadir}/doc/wayland/

%files -n libwayland-client
%license COPYING
%{_libdir}/libwayland-client.so.0*

%files -n libwayland-cursor
%license COPYING
%{_libdir}/libwayland-cursor.so.0*

%files -n libwayland-egl
%license COPYING
%{_libdir}/libwayland-egl.so.1*

%files -n libwayland-server
%license COPYING
%{_libdir}/libwayland-server.so.0*

%changelog
* Sat May 10 2025 Thomas Mecattaf <thomas@mecattaf.dev> - 1.23.1-1
- Update to 1.23.1
