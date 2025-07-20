Name:           fabric
Version:        0.0.1
Release:        %autorelease
Summary:        Next-generation framework for building desktop widgets using Python

License:        AGPL-3.0-or-later
URL:            https://github.com/Fabric-Development/fabric
Source0:        %{url}/archive/refs/heads/master.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

# Runtime GTK/GI dependencies
BuildRequires:  gtk3-devel
BuildRequires:  cairo-devel
BuildRequires:  gtk-layer-shell-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  libdbusmenu-gtk3-devel

# Python dependencies
Requires:       python3
Requires:       python3-gobject
Requires:       python3-cairo
Requires:       python3-click
Requires:       python3-loguru

# GTK/System dependencies
Requires:       gtk3
Requires:       cairo
Requires:       gtk-layer-shell
Requires:       libgirepository
Requires:       gobject-introspection
Requires:       webkit2gtk4.1
Requires:       libdbusmenu-gtk3

# Optional but recommended dependencies
Recommends:     python3-psutil
Recommends:     pkgconf

# For audio functionality (optional)
Suggests:       cinnamon-desktop

# For examples and full functionality
Suggests:       wl-clipboard
Suggests:       python3-requests

%description
Fabric is a Desktop Widgets System that you can customize using Python. 
It offers a variety of features to make the often tedious process of creating 
widgets much easier and more enjoyable!

Key features:
- Simple yet Powerful
- Supports both X11 and Wayland  
- Access to all other Python modules
- Excellent Developer Experience (DevEX) and typing support
- Low resource usage
- Built-in Python code replaces the need for resource-heavy shell scripts

%prep
%autosetup -n fabric-master

%build
%py3_build

%install
%py3_install

# Install example configurations
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -r examples/* %{buildroot}%{_datadir}/%{name}/examples/

# Install documentation
mkdir -p %{buildroot}%{_docdir}/%{name}
cp README.md %{buildroot}%{_docdir}/%{name}/
cp CHANGELOG.md %{buildroot}%{_docdir}/%{name}/ 2>/dev/null || true

%files
%license LICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%{_bindir}/fabric
%{python3_sitelib}/fabric/
%{python3_sitelib}/fabric-*.egg-info/
%{_datadir}/%{name}/examples/

%changelog
* %{?date:%{date}}%{!?date:%(date +"%%a %%b %%d %%Y")} Package Maintainer <maintainer@example.com> - 0.0.2-1
- Initial RPM package for Fabric
- Includes all core dependencies and example configurations
- Supports both X11 and Wayland environments
%autochangelog
