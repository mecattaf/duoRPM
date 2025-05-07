%global debug_package %{nil}

Name:           eza
Version:        0.21.3
Release:        %autorelease
Summary:        A modern alternative to ls

License:        EUPL-1.2
URL:            https://github.com/eza-community/eza
Source0:        %{url}/releases/download/v%{version}/%{name}_x86_64-unknown-linux-gnu.tar.gz
Source1:        %{url}/releases/download/v%{version}/completions-%{version}.tar.gz
Source2:        %{url}/releases/download/v%{version}/man-%{version}.tar.gz
Source3:        https://raw.githubusercontent.com/eza-community/eza/v%{version}/LICENSE.txt

BuildArch:      x86_64
BuildRequires:  gzip

%description
eza is a modern, maintained replacement for the ls command.

- It uses colors to distinguish file types and metadata.
- It recognizes symlinks, extended attributes, and Git status.
- It's written in Rust, so it's small, fast, and portable.

%prep
%autosetup -c
# Extract additional tarballs manually to specific directories
mkdir -p completions-%{version}
mkdir -p man-%{version}
tar -xf %{SOURCE1} -C completions-%{version}
tar -xf %{SOURCE2} -C man-%{version}
cp %{SOURCE3} .

%build
# Find and compress man pages properly
find man-%{version} -name "*.1" -exec gzip -9 {} \;
find man-%{version} -name "*.5" -exec gzip -9 {} \;

%install
# Install binary
install -Dpm755 %{name} %{buildroot}%{_bindir}/%{name}

# Install shell completions
install -Dpm644 completions-%{version}/%{name} %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dpm644 completions-%{version}/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dpm644 completions-%{version}/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

# Install man pages - using find to locate them regardless of directory structure
for manpage in $(find man-%{version} -name "%{name}.1.gz"); do
    install -Dpm644 "$manpage" %{buildroot}%{_mandir}/man1/%{name}.1.gz
done

for manpage in $(find man-%{version} -name "%{name}_colors.5.gz"); do
    install -Dpm644 "$manpage" %{buildroot}%{_mandir}/man5/%{name}_colors.5.gz
done

for manpage in $(find man-%{version} -name "%{name}_colors-explanation.5.gz"); do
    install -Dpm644 "$manpage" %{buildroot}%{_mandir}/man5/%{name}_colors-explanation.5.gz
done

# Create ls symlink
ln -sf %{name} %{buildroot}%{_bindir}/exa

%files
%license LICENSE.txt
%{_bindir}/%{name}
%{_bindir}/exa
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}_colors.5.gz
%{_mandir}/man5/%{name}_colors-explanation.5.gz

%changelog
* Thu May 08 2025 Package Maintainer <maintainer@example.com> - 0.21.3-1
- Update to version 0.21.3
%autochangelog
