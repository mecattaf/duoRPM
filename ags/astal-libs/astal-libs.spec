%global astal_commit 7f2292f0792ffc9b127d4788b3dd3f104b5374b2
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 14

%global _lto_cflags %{nil}

Name:           astal-libs
Version:        0.1.0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        Astal service libraries for desktop shells

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/astal-%{astal_shortcommit}.tar.gz
Source1:        https://github.com/LukashonakV/cava/archive/0.10.3.tar.gz

BuildRequires:  gcc
BuildRequires:  iniparser-devel
BuildRequires:  meson >= 0.59.0
BuildRequires:  vala
BuildRequires:  valadoc
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(appmenu-glib-translator)
BuildRequires:  pkgconfig(astal-3.0)
BuildRequires:  pkgconfig(astal-4-4.0)
BuildRequires:  pkgconfig(astal-io-0.1)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(wireplumber-0.5)

# Runtime dependencies
Requires:       astal%{?_isa} = %{version}-%{release}
Requires:       astal-gtk4%{?_isa} = %{version}-%{release}
Requires:       astal-io%{?_isa} = %{version}-%{release}

# Optional runtime dependencies for full functionality
Recommends:     bluez
Recommends:     NetworkManager
Recommends:     pipewire
Recommends:     wireplumber
Recommends:     upower

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%description
Astal service libraries provide modules to work with system services like:
- Network and Bluetooth management
- Battery monitoring
- Audio control via PipeWire/PulseAudio
- Media player control (MPRIS)
- System tray
- Notifications
- Hyprland and River compositor integration
- Authentication
- Power profiles

%prep
%autosetup -n astal-%{astal_commit} -p1
# Extract cava for audio visualization
tar -xf %{SOURCE1} -C lib/cava/subprojects

%build
cd lib
# Build each library separately
for lib in apps auth battery bluetooth cava greet hyprland mpris network notifd power-profiles river tray wireplumber; do
    if [ -d "$lib" ]; then
        pushd $lib
        %meson --auto-features=auto
        %meson_build
        popd
    fi
done

%install
cd lib
for lib in apps auth battery bluetooth cava greet hyprland mpris network notifd power-profiles river tray wireplumber; do
    if [ -d "$lib" ]; then
        pushd $lib
        %meson_install
        popd
    fi
done

# Fix cava pkgconfig file if needed
if [ -f %{buildroot}%{_libdir}/pkgconfig/astal-cava-0.1.pc ]; then
    sed -i 's/ cava,//' %{buildroot}%{_libdir}/pkgconfig/astal-cava-0.1.pc
fi

# Remove duplicate cava files if they exist
rm -rf %{buildroot}%{_includedir}/cava
rm -rf %{buildroot}%{_datadir}/consolefonts/cava.psf
rm -rf %{buildroot}%{_libdir}/pkgconfig/cava.pc

%files
%license LICENSE
%config(noreplace) /etc/pam.d/astal-auth
# Binaries
%{_bindir}/astal-apps
%{_bindir}/astal-auth
%{_bindir}/astal-battery
%{_bindir}/astal-greet
%{_bindir}/astal-hyprland
%{_bindir}/astal-mpris
%{_bindir}/astal-notifd
%{_bindir}/astal-power-profiles
%{_bindir}/astal-river
%{_bindir}/astal-tray
# Libraries
%{_libdir}/libastal-apps.so.0*
%{_libdir}/libastal-auth.so.0*
%{_libdir}/libastal-battery.so.0*
%{_libdir}/libastal-bluetooth.so.0*
%{_libdir}/libastal-cava.so.0*
%{_libdir}/libastal-greet.so.0*
%{_libdir}/libastal-hyprland.so.0*
%{_libdir}/libastal-mpris.so.0*
%{_libdir}/libastal-network.so.0*
%{_libdir}/libastal-notifd.so.0*
%{_libdir}/libastal-power-profiles.so.0*
%{_libdir}/libastal-river.so.0*
%{_libdir}/libastal-tray.so.0*
%{_libdir}/libastal-wireplumber.so.0*
%{_libdir}/libcava.so
# GObject Introspection
%{_libdir}/girepository-1.0/AstalApps-0.1.typelib
%{_libdir}/girepository-1.0/AstalAuth-0.1.typelib
%{_libdir}/girepository-1.0/AstalBattery-0.1.typelib
%{_libdir}/girepository-1.0/AstalBluetooth-0.1.typelib
%{_libdir}/girepository-1.0/AstalCava-0.1.typelib
%{_libdir}/girepository-1.0/AstalGreet-0.1.typelib
%{_libdir}/girepository-1.0/AstalHyprland-0.1.typelib
%{_libdir}/girepository-1.0/AstalMpris-0.1.typelib
%{_libdir}/girepository-1.0/AstalNetwork-0.1.typelib
%{_libdir}/girepository-1.0/AstalNotifd-0.1.typelib
%{_libdir}/girepository-1.0/AstalPowerProfiles-0.1.typelib
%{_libdir}/girepository-1.0/AstalRiver-0.1.typelib
%{_libdir}/girepository-1.0/AstalTray-0.1.typelib
%{_libdir}/girepository-1.0/AstalWp-0.1.typelib

%files devel
%{_datadir}/gir-1.0/Astal*-0.1.gir
%{_datadir}/vala/vapi/astal-*-0.1.deps
%{_datadir}/vala/vapi/astal-*-0.1.vapi
%{_includedir}/astal-*.h
%{_includedir}/astal/
%{_libdir}/libastal-apps.so
%{_libdir}/libastal-auth.so
%{_libdir}/libastal-battery.so
%{_libdir}/libastal-bluetooth.so
%{_libdir}/libastal-cava.so
%{_libdir}/libastal-greet.so
%{_libdir}/libastal-hyprland.so
%{_libdir}/libastal-mpris.so
%{_libdir}/libastal-network.so
%{_libdir}/libastal-notifd.so
%{_libdir}/libastal-power-profiles.so
%{_libdir}/libastal-river.so
%{_libdir}/libastal-tray.so
%{_libdir}/libastal-wireplumber.so
%{_libdir}/pkgconfig/astal-*.pc

%changelog
%autochangelog
