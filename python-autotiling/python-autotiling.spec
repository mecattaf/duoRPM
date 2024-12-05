# source: https://copr-dist-git.fedorainfracloud.org/cgit/tofik/sway-tools/python-autotiling.git/tree/python-autotiling.spec
# Created by pyp2rpm-3.3.10
%global pypi_name autotiling
%global pypi_version 1.9.3

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Automatically switch the horizontal/vertical window split orientation in sway and i3

License:        GPL-3.0-or-later
URL:            https://github.com/nwg-piotr/autotiling
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(setuptools) >= 42
BuildRequires:  python3dist(wheel)

%description
This script uses the i3ipc-python library to switch the layout splith/splitv 
depending on the currently focused window dimensions. It works on both sway 
and i3 window managers.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(i3ipc)
Requires:       python3dist(importlib-metadata)
Requires:       python3dist(setuptools)

%description -n python3-%{pypi_name}
This script uses the i3ipc-python library to switch the layout splith/splitv 
depending on the currently focused window dimensions. It works on both sway 
and i3 window managers.

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/autotiling
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Mon Nov 11 2024 mockbuilder - 1.9.3-1
- Initial package.
