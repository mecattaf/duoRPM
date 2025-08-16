# Use git snapshot since no releases exist yet
%global commit          860232f34a77837915a94078efe8cd527fa582e3
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapdate        20240727

Name:           wlvncc
Version:        0.1.0~git%{snapdate}.%{shortcommit}
Release:        1%{?dist}
Summary:        Wayland native VNC client

License:        ISC
URL:            https://github.com/any1/wlvncc
# Use git snapshot since no releases exist yet
Source0:        https://github.com/any1/wlvncc/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aml)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

# Optional dependencies that enable additional features
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libsasl2)
BuildRequires:  pkgconfig(zlib)
# Note: lzo2 might not be available, making it optional
%{?_with_lzo:BuildRequires: pkgconfig(lzo2)}

Requires:       wayland
Requires:       mesa-dri-drivers

%description
This is a work-in-progress implementation of a Wayland native VNC client.
Expect bugs and missing features.

Features:
- Wayland native implementation
- Hardware acceleration support via GBM/EGL
- Multiple encoding support (Raw, RRE, CoRRE, Hextile, Zlib, Tight, TRLE, ZRLE)
- H.264 video encoding support via FFmpeg
- Authentication support (VNC Auth, VeNCrypt, SASL)
- TLS encryption support
- Keyboard shortcuts inhibition
- Multiple pixel formats

%prep
%autosetup -n %{name}-%{commit}

%build
%meson \
    -Dexamples=false
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}

%changelog
* Wed Jul 27 2024 Automated Build <builder@copr.fedoraproject.org> - 0.1.0~git20240727.860232f-1
- Initial package for wlvncc using git snapshot from July 27, 2024
- Wayland native VNC client with hardware acceleration support
