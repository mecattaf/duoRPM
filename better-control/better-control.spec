%global forgeurl https://github.com/quantumvoid0/better-control
Version:        6.11.4
%forgemeta

Name:           better-control
Release:        %autorelease
Summary:        A sleek GTK-themed control panel for Linux

License:        GPL-3.0-only
URL:            %{forgeurl}
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

# Build dependencies
BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel

# Runtime dependencies based on PKGBUILD and README.md
Requires:       gtk3
Requires:       NetworkManager
Requires:       python3-gobject
Requires:       python3-dbus
Requires:       python3-psutil
Requires:       python3-setproctitle
Requires:       python3-qrcode
Requires:       python3-pillow
Requires:       python3-requests
Requires:       power-profiles-daemon
Requires:       brightnessctl
Requires:       upower
Requires:       gammastep

# Optional dependencies that provide additional functionality
Recommends:     bluez
Recommends:     bluez-utils
Recommends:     pipewire-pulse
Recommends:     usbguard

# Conflicts/Provides (if a -git variant is added later)
Provides:       %{name} = %{version}-%{release}

%description
Better Control is a sleek GTK-themed control panel for Linux. It provides
a modern, clean interface for system controls including:

- WiFi network management with connection speed monitoring
- Bluetooth device management with auto-connecting
- Volume control for speakers, microphones, and per-application audio
- Screen brightness adjustment
- Display orientation control
- Battery monitoring and power profiles
- Blue light filtering (Night Light)
- Autostart application management
- USBGuard device control

It works seamlessly across multiple desktop environments and window managers,
with particular focus on Wayland compositors like Hyprland and Sway.
The interface respects your system's light/dark theme settings.

%prep
%autosetup

%build
# Nothing to build for Python application

%install
# Create directory structure
install -dm755 %{buildroot}%{_datadir}/%{name}
install -dm755 %{buildroot}%{_bindir}
install -dm755 %{buildroot}%{_datadir}/applications

# Install the betterctl script
install -Dm755 betterctl.sh %{buildroot}%{_bindir}/betterctl

# Copy all source files to share directory
cp -r src/* %{buildroot}%{_datadir}/%{name}/

# Install main Python script
install -Dm755 src/better_control.py %{buildroot}%{_datadir}/%{name}/better_control.py

# Create the executable script
echo '#!/bin/bash' > %{buildroot}%{_bindir}/%{name}
echo 'python3 %{_datadir}/%{name}/better_control.py "$@"' >> %{buildroot}%{_bindir}/%{name}
chmod 755 %{buildroot}%{_bindir}/%{name}

# Create control symlink
ln -sf %{name} %{buildroot}%{_bindir}/control

# Install desktop file
sed 's|Exec=/usr/bin/control|Exec=/usr/bin/better-control|' \
    src/control.desktop > %{buildroot}%{_datadir}/applications/%{name}.desktop

# Verify desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/control
%{_bindir}/betterctl
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop

%changelog
- Initial package for Fedora COPR repository
