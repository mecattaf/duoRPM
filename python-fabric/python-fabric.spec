%global pypi_name fabric
%global forgeurl https://github.com/Fabric-Development/fabric

Name:           python-%{pypi_name}
Version:        0.0.2
Release:        1%{?dist}
Summary:        Next-Gen framework for building desktop widgets using Python

License:        AGPL-3.0-or-later
URL:            %{forgeurl}
# Use git source directly like in PKGBUILD
Source0:        %{url}.git

BuildArch:      noarch

BuildRequires:  git-core
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
BuildRequires:  python3-gobject-devel

Requires:       python3-gobject
Requires:       python3-cairo
Requires:       python3-click
Requires:       python3-loguru
Requires:       gtk3
Requires:       gtk-layer-shell
Requires:       cairo
Requires:       gobject-introspection
Requires:       libdbusmenu-gtk3
Requires:       webkit2gtk4.0

# Optional dependencies
Recommends:     python3-psutil
Recommends:     gnome-bluetooth

%description
Fabric is a Desktop Widgets System that can be customized using Python. It offers
a variety of features to make the often tedious process of creating widgets much
easier and more enjoyable. It supports both X11 and Wayland display servers with
a high-level, signal-based workflow pattern that eliminates the need for polling
or bash scripting for basic tasks.

%prep
# Use git clone like in PKGBUILD
%setup -q -T -c
git clone %{url} .
# Optional: checkout a specific tag if needed
# git checkout v%{version}

%build
%py3_build

%install
%py3_install
# List the files for debugging
find %{buildroot} -type f -o -type l | sort

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/fabric/
# Use a wildcard pattern that will match either egg-info or dist-info
%{python3_sitelib}/fabric-*
