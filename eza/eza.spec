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
# Extract additional tarballs manually
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
cp %{SOURCE3} .

%build
# Compress man pages
gzip -9 man-%{version}/*.1
gzip -9 man-%{version}/*.5

%install
# Install binary
install -Dpm755 %{name} %{buildroot}%{_bindir}/%{name}

# Install shell completions
install -Dpm644 completions-%{version}/%{name} %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dpm644 completions-%{version}/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dpm644 completions-%{version}/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

# Install man pages
install -Dpm644 man-%{version}/%{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz
install -Dpm644 man-%{version}/%{name}_colors.5.gz %{buildroot}%{_mandir}/man5/%{name}_colors.5.gz
install -Dpm644 man-%{version}/%{name}_colors-explanation.5.gz %{buildroot}%{_mandir}/man5/%{name}_colors-explanation.5.gz

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
%autochangelog
