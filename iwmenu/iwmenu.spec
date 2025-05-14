%global debug_package %{nil}

Name:           iwmenu
Version:        0.2.0
Release:        1%{?dist}
Summary:        Launcher-driven Wi-Fi manager for Linux

License:        GPL-3.0
URL:            https://github.com/e-tho/iwmenu
Source0:        %{url}/releases/download/v%{version}/%{name}-x86_64-linux-gnu
Source1:        %{url}/releases/download/v%{version}/LICENSE.md
Source2:        %{url}/releases/download/v%{version}/README.md
Source3:        %{url}/releases/download/v%{version}/CONTRIBUTING.md

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
cp %{SOURCE1} LICENSE.md
cp %{SOURCE2} README.md
cp %{SOURCE3} CONTRIBUTING.md

%build
# Nothing to build - using prebuilt binary

%install
# Install binary
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

# Generate and install shell completions if the binary supports it
if ./%{name} --help | grep -q completion; then
  mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
  mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
  mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
  
  ./%{name} completion bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name} || :
  ./%{name} completion fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish || :
  ./%{name} completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name} || :
fi

%files
%license LICENSE.md
%doc README.md CONTRIBUTING.md
%{_bindir}/%{name}
%if 0%{?_datadir:1}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%endif

%changelog
* Tue May 13 2025 Package Maintainer <maintainer@example.com> - 0.2.0-1
- Initial package
