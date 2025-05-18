%global commit ed43b332d4f93c955d825256e6ef9e9bcdbd297e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20250510
%global snap %{commit_date}git%{shortcommit}

Name:           scroll
Version:        0.1.0~%{snap}
Release:        0.1%{?dist}
Summary:        Wayland compositor with a scrolling layout forked from sway

License:        MIT
URL:            https://github.com/dawsers/scroll
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source100:      config.minimal
Source101:      scroll-portals.conf

# Conditional patches

BuildRequires:  gcc-c++
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
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(wlroots-0.19)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0

# Require any of the available configuration packages;
# Prefer the -upstream one if none are directly specified in the package manager transaction
Requires:       %{name}-config
Suggests:       %{name}-config-upstream

%description
Scroll is a tiling window manager supporting Wayland compositor protocol and 
sway/i3-compatible configuration. The main difference is scroll only supports 
one layout, a scrolling layout similar to PaperWM, niri or hyprscroller.

Scroll adds features such as:
- Animations with customizable N-order Bezier curves
- Independent content scaling for individual Wayland windows
- Overview and Jump modes for window management
- Workspace scaling
- Trackpad/Mouse scrolling navigation
- Support for both portrait and landscape monitor orientations

# Configuration presets:
#
%package        config-upstream
Summary:        Upstream configuration for Scroll
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-config = %{version}-%{release}
Conflicts:      %{name}-config

# Require the wallpaper referenced in the config.
# Weak dependency here causes a scrollnag warning during the configuration load
Requires:       sway-wallpapers
# Lack of graphical drivers may hurt the common use case
Requires:       mesa-dri-drivers
# Logind needs polkit to create a graphical session
Requires:       polkit
# swaybg is used in the default config
Requires:       swaybg
# dmenu (as well as rxvt any many others) requires XWayland on Sway
Requires:       xorg-x11-server-Xwayland

# Scroll binds the terminal shortcut to one specific terminal. In our case foot
Recommends:     foot
# grim is the recommended way to take screenshots on wayland
Recommends:     grim
# wmenu is the default launcher in sway/scroll
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
%autosetup -n %{name}-%{commit}

%build
%meson \
    -Dsd-bus-provider=libsystemd \
    -Dwerror=false
%meson_build

%install
%meson_install
# Install minimal configuration file
install -D -m644 -pv %{SOURCE100} %{buildroot}%{_sysconfdir}/%{name}/config.minimal
# Install portals.conf for xdg-desktop-portal
install -D -m644 -pv %{SOURCE101} %{buildroot}%{_datadir}/xdg-desktop-portal/%{name}-portals.conf
# install the documentation
install -D -m644 -pv README.md    %{buildroot}%{_pkgdocdir}/README.md
install -D -m644 -pv %{SOURCE102} %{buildroot}%{_pkgdocdir}/README.Fedora
# Create directory for extra config snippets
install -d -m755 -pv %{buildroot}%{_sysconfdir}/%{name}/config.d

%files
%license LICENSE
%doc %{_pkgdocdir}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/config.d
%{_mandir}/man1/%{name}*
%{_mandir}/man5/*
%{_mandir}/man7/*
%caps(cap_sys_nice=ep) %{_bindir}/%{name}
%{_bindir}/%{name}bar
%{_bindir}/%{name}msg
%{_bindir}/%{name}nag
%dir %{_datadir}/xdg-desktop-portal
%{_datadir}/xdg-desktop-portal/%{name}-portals.conf
%{bash_completions_dir}/%{name}*
%{fish_completions_dir}/%{name}*.fish
%{zsh_completions_dir}/_%{name}*

%files config-upstream
%config(noreplace) %{_sysconfdir}/%{name}/config
%{_datadir}/wayland-sessions/%{name}.desktop

%files config-minimal
%config(noreplace) %{_sysconfdir}/%{name}/config.minimal

%changelog
* Sat May 10 2025 Thomas Mecattaf <thomas@mecattaf.dev> - 0.1.0~20250510gited43b3-0.1
- Initial package of scroll using git snapshot
