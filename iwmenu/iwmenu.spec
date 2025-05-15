%global debug_package %{nil}

Name:           iwmenu
Version:        0.2.0
Release:        1%{?dist}
Summary:        Launcher-driven Wi-Fi manager for Linux

License:        GPL-3.0
URL:            https://github.com/e-tho/iwmenu
Source0:        %{url}/releases/download/v%{version}/%{name}-x86_64-linux-gnu

# This is a prebuilt binary package, only available for x86_64
ExclusiveArch:  x86_64
Requires:       glibc
Requires:       iwd
Requires:       dbus

%description
iwmenu (iNet Wireless Menu) manages Wi-Fi through your launcher of choice.

It provides:
- Wi-Fi network scanning and connection
- Known network management
- Connection information display
- Access point mode configuration
- Support for various launchers (dmenu, rofi, fuzzel, walker)
- Both font-based and XDG icon support

%prep
# No need for standard setup since we're using prebuilt binaries
%setup -q -c -T
cp %{SOURCE0} %{name}

%build
# Nothing to build - using prebuilt binary

%install
# Install binary
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%changelog
* Tue May 13 2025 Package Maintainer <maintainer@example.com> - 0.2.0-1
- Initial package
