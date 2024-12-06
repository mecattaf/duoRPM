# Theme packaging for GTK environments
# Source: https://github.com/catppuccin/gtk

Name:           catppuccin-theme
Version:        1.0.3
Release:        1%{?dist}
Summary:        Catppuccin themes and icons for GTK environments

License:        MIT
URL:            https://github.com/catppuccin/gtk
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  sassc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel

Requires:       gtk3
Requires:       gtk4
Recommends:     gtk-murrine-engine

%description
Soothing pastel theme for GTK3/4 and various applications. The Catppuccin theme
provides a warm and cozy aesthetic for your desktop environment with multiple
flavors: Mocha, Macchiato, Frappé, and Latte.

%prep
%autosetup -n gtk-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_datadir}/themes/Catppuccin-*

%changelog
* Thu Dec 05 2024 Maintainer <thomasmecattaf@gmail.com> - 0.7.1-1
- Initial package for zenRPM repository
