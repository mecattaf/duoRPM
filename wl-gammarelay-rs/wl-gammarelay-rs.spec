Name:           wl-gammarelay-rs
Version:        1.0.0
Release:        %autorelease
Summary:        Wayland display temperature and brightness control via DBus

License:        GPL-3.0-only
URL:            https://github.com/MaxVerevkin/wl-gammarelay-rs
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  rust
BuildRequires:  cargo

%description
A simple program that provides DBus interface to control display temperature 
and brightness under wayland without flickering. Can be used as an alternative 
to redshift/gammastep.

%prep
%autosetup
cargo vendor
%cargo_prep -v vendor

%build
cargo build --locked --profile rpm

%install
rm -rf %{buildroot}
install -Dpm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Wed Dec 04 2024 Maintainer <thomasmecattaf@gmail.com> - 1.0.0
- Initial release using GitHub releases
