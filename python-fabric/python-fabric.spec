%global pypi_name fabric
%global forgeurl https://github.com/Fabric-Development/fabric
# Using commit for main branch since there are no proper release tags
%global commit 67e6c1f5daf60fc28be329f9a40d9e07e0cfb8e3
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{pypi_name}
Version:        0.0.2
Release:        1%{?dist}
Summary:        Next-Gen framework for building desktop widgets using Python

License:        AGPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/%{commit}/%{pypi_name}-%{commit}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  gtk-layer-shell-devel
BuildRequires:  cairo-devel
BuildRequires:  libdbusmenu-gtk3-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-pygobject3-devel

Requires:       python3-gobject
Requires:       python3-cairo
Requires:       python3-click
Requires:       python3-loguru
Requires:       gtk3
Requires:       gtk-layer-shell
Requires:       cairo
Requires:       gobject-introspection
Requires:       libdbusmenu-gtk3
Requires:       webkit2gtk4.1

# Optional dependencies
Recommends:     python3-psutil
Recommends:     gnome-bluetooth3

%description
Fabric is a Desktop Widgets System that can be customized using Python. It offers
a variety of features to make the often tedious process of creating widgets much
easier and more enjoyable. It supports both X11 and Wayland display servers with
a high-level, signal-based workflow pattern that eliminates the need for polling
or bash scripting for basic tasks.

%prep
%autosetup -n %{pypi_name}-%{commit}
# Ensure that we don't try to regenerate docs during the build process
if [ -f docs/Makefile ]; then
    touch docs/Makefile
fi

%build
%py3_build

%install
%py3_install
# Remove bundled egg-info if it exists
rm -rf %{buildroot}%{python3_sitelib}/fabric-*.egg-info

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/fabric/
%{python3_sitelib}/fabric-*.egg-info/

%changelog
* Tue Mar 18 2025 Automated Package Build <builder@copr.fedoraproject.org> - 0.0.2-1
- Initial package for Fedora COPR
