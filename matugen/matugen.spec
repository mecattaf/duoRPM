Name:           matugen
Version:        0.13.0
Release:        %autorelease
Summary:        Fast and simple wallpaper-based palette generator written in Rust

License:        GPL-3.0-or-later
URL:            https://github.com/InfernoEmbedded/matugen
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  rust-packaging

# Optional deps (if any native libs appear later in build)
BuildRequires:  pkg-config
BuildRequires:  clang

Requires:       desktop-file-utils

%description
Matugen is a fast and simple wallpaper-based palette generator written in Rust. It can
generate colorschemes from wallpapers or images and is compatible with various formats
like Pywal, GTK themes, and more.

%prep
%autosetup -n %{name}-%{version}
%{__cargo} vendor

mkdir -p .cargo
cat > .cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%{__cargo} build --release

%install
install -Dpm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
%autochangelog
