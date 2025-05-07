%global debug_package %{nil}

Name:           atuin
Version:        18.6.0
Release:        %autorelease
Summary:        Magical shell history

License:        MIT
URL:            https://github.com/atuinsh/atuin
Source0:        %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-musl.tar.gz
Source1:        https://raw.githubusercontent.com/atuinsh/atuin/v%{version}/README.md
Source2:        https://raw.githubusercontent.com/atuinsh/atuin/v%{version}/LICENSE

BuildArch:      x86_64
Requires:       glibc

%global         _missing_build_ids_terminate_build 0
ExclusiveArch:  x86_64

%description
Atuin replaces your existing shell history with a SQLite database, and records additional context for your commands.
Additionally, it provides optional and fully encrypted synchronization of your history between machines, via an Atuin server.

%prep
%autosetup -c
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
# Binary release, nothing to build

%install
# Install binary
install -Dpm755 %{name} %{buildroot}%{_bindir}/%{name}

# Install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

%{buildroot}%{_bindir}/%{name} completions bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name}
%{buildroot}%{_bindir}/%{name} completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{buildroot}%{_bindir}/%{name} completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}

%changelog
* Thu May 08 2025 Package Maintainer <maintainer@example.com> - 18.6.0-1
- Update to version 18.6.0
%autochangelog
