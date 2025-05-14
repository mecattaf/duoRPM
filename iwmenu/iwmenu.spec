Name:           iwmenu
Version:        0.2.0
Release:        1%{?dist}
Summary:        Launcher-driven Wi-Fi manager for Linux

License:        GPL-3.0
URL:            https://github.com/e-tho/iwmenu
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(dbus-1)

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
%autosetup
# Set up cargo vendor configuration
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 9
%cargo_prep
%else
# For older distros that don't have cargo_prep
%{__cargo} vendor
mkdir -p .cargo
cat > .cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
%endif

%build
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 9
%cargo_build
%else
# For older distros that don't have cargo_build
%{__cargo} build --release %{?_smp_mflags}
%endif

%install
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 9
%cargo_install
%else
# For older distros that don't have cargo_install
install -Dpm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
%endif

%files
%license LICENSE.md
%doc README.md CONTRIBUTING.md
%{_bindir}/%{name}

%changelog
* Tue May 13 2025 Package Maintainer <maintainer@example.com> - 0.2.0-1
- Initial package
