# Use git snapshot since no releases exist yet
%global commit          860232f34a77837915a94078efe8cd527fa582e3
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapdate        20240727

# aml version needed for bundling
%global aml_version     1.0.0

Name:           wlvncc
Version:        0.1.0~git%{snapdate}.%{shortcommit}
Release:        1%{?dist}
Summary:        Wayland native VNC client

License:        ISC and GPL-2.0-or-later
URL:            https://github.com/any1/wlvncc
# Use git snapshot since no releases exist yet
Source0:        https://github.com/any1/wlvncc/archive/%{commit}/%{name}-%{commit}.tar.gz
# Bundle aml v1.0.0 since it's not available in Fedora repos yet
Source1:        https://github.com/any1/aml/archive/refs/tags/v%{aml_version}/aml-%{aml_version}.tar.gz
# Get minilzo from the full LZO source (minilzo is part of it)
Source2:        http://www.oberhumer.com/opensource/lzo/download/lzo-2.10.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.50.0
BuildRequires:  ninja-build
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

Requires:       wayland
Requires:       mesa-dri-drivers

# Bundled libraries
Provides:       bundled(aml) = %{aml_version}
Provides:       bundled(minilzo) = 2.10

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
# Extract and setup bundled aml as subproject
tar -xf %{SOURCE1}
# Create subprojects directory if it doesn't exist
mkdir -p subprojects
mv aml-%{aml_version} subprojects/aml

# Extract LZO and copy minilzo files
tar -xf %{SOURCE2}
# Copy minilzo files from the full LZO distribution
cp lzo-2.10/minilzo/minilzo.c src/encodings/
cp lzo-2.10/minilzo/minilzo.h src/encodings/
# Copy required header files that minilzo depends on
cp lzo-2.10/include/lzo/lzoconf.h src/encodings/
cp lzo-2.10/include/lzo/lzodefs.h src/encodings/
# If there are any other required headers, copy them too
for header in lzoutil.h lzo1x.h; do
    [ -f "lzo-2.10/include/lzo/$header" ] && cp "lzo-2.10/include/lzo/$header" src/encodings/
done

# Fix include paths in the copied files to use local versions
sed -i 's|#include "lzo/|#include "|g' src/encodings/*.h 2>/dev/null || true
sed -i 's|#include <lzo/|#include "|g' src/encodings/*.h 2>/dev/null || true

%build
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}

%changelog
* Sat Aug 16 2025 Automated Build <builder@copr.fedoraproject.org> - 0.1.0~git20240727.860232f-1
- Initial package for wlvncc using git snapshot from July 27, 2024
- Wayland native VNC client with hardware acceleration support
- Bundle minilzo from LZO 2.10 for compression support
