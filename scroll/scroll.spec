%global commit   %(git ls-remote https://github.com/dawsers/scroll HEAD | cut -f1)
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate %(date +"%Y%m%d")

Name:           scroll
Version:        0.0.1^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Wayland compositor with scrolling layout based on Sway
License:        MIT
URL:            https://github.com/dawsers/scroll
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Minimal configuration file for headless or buildroot use
Source100:      config.minimal
Source101:      scroll-portals.conf
Source102:      README.Fedora.md

# Upstream patches

# Fedora patches

# Conditional patches

BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  meson >= 0.60.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(json-c) >= 0.13
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput) >= 1.26.0
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libsystemd) >= 239
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server) >= 1.21.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.24
BuildRequires:  pkgconfig(wlroots) >= 0.18.0
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libseat)

# Require any of the available configuration packages;
# Prefer the -upstream one if none are directly specified in the package manager transaction
Requires:       %{name}-config
Suggests:       %{name}-config-upstream

%description
Scroll is a tiling window manager supporting Wayland compositor protocol and
i3-compatible configuration, forked from Sway. The main difference is scroll
only supports one layout, a scrolling layout similar to PaperWM.

Scroll offers additional features:
* Animations with customizable N-order Bezier curves
* Independent content scaling for individual windows
* Overview and Jump modes for efficient window management
* Workspace scaling for improved navigation
* Trackpad/Mouse scrolling for workspace navigation


# Configuration presets:
#
%package        config-upstream
Summary:        Upstream configuration for Scroll
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config

# Lack of graphical drivers may hurt the common use case
Requires:       mesa-dri-drivers
# Logind needs polkit to create a graphical session
Requires:       polkit
# dmenu (as well as rxvt any many others) requires XWayland on Scroll
Requires:       xorg-x11-server-Xwayland

# Scroll binds the terminal shortcut to one specific terminal. In our case foot
Recommends:     foot
# grim is the recommended way to take screenshots on sway-based environments
Recommends:     grim
# wmenu is the default launcher in scroll
Recommends:     wmenu
# Install configs and scripts for better integration with systemd user session
Recommends:     sway-systemd
# Both utilities are suggested in the default configuration
Recommends:     swayidle
Recommends:     swaylock

# Minimal installation doesn't include Qt Wayland backend
Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description    config-upstream
Upstream configuration for Scroll.
Includes all important dependencies for a typical desktop system
with minimal or no divergence from the upstream.


%package        config-minimal
RemovePathPostfixes:  .minimal
Summary:        Minimal configuration for Scroll
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config
# List of dependencies for headless or buildroot use

%description    config-minimal
Minimal configuration for Scroll without any extra dependencies.
Suitable for headless or buildroot use.


%prep
%autosetup -n %{name}-%{commit} -p1
# apply unconditional patches
#autopatch -p1 -M99
# apply conditional patches

%build
%meson \
    -Dsd-bus-provider=libsystemd \
    -Dtray=enabled \
    -Dwerror=false
%meson_build

%install
%meson_install
# Install minimal configuration file
install -D -m644 -pv %{SOURCE100} %{buildroot}%{_sysconfdir}/scroll/config.minimal
# Install portals.conf for xdg-desktop-portal
install -D -m644 -pv %{SOURCE101} %{buildroot}%{_datadir}/xdg-desktop-portal/scroll-portals.conf
# install the documentation
install -D -m644 -pv README.md    %{buildroot}%{_pkgdocdir}/README.md
install -D -m644 -pv %{SOURCE102} %{buildroot}%{_pkgdocdir}/README.Fedora
# Create directory for extra config snippets
install -d -m755 -pv %{buildroot}%{_sysconfdir}/scroll/config.d

%files
%license LICENSE
%doc %{_pkgdocdir}
%dir %{_sysconfdir}/scroll
%dir %{_sysconfdir}/scroll/config.d
%{_mandir}/man1/scroll*
%{_mandir}/man5/*
%{_mandir}/man7/*
%caps(cap_sys_nice=ep) %{_bindir}/scroll
%{_bindir}/scrollbar
%{_bindir}/scrollmsg
%{_bindir}/scrollnag
%dir %{_datadir}/xdg-desktop-portal
%{_datadir}/xdg-desktop-portal/scroll-portals.conf
%{bash_completions_dir}/scroll*
%{fish_completions_dir}/scroll*.fish
%{zsh_completions_dir}/_scroll*

%files config-upstream
%config(noreplace) %{_sysconfdir}/scroll/config
%{_datadir}/wayland-sessions/scroll.desktop

%files config-minimal
%config(noreplace) %{_sysconfdir}/scroll/config.minimal

%changelog
* Thu May 08 2025 Packager <packager@example.com> - 0.0.1^20250508git1234567-1
- Initial package of scroll from git
