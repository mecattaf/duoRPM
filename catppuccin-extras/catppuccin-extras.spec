%global debug_package %{nil}

Name:           catppuccin-extras
Version:        1.0.0
Release:        1%{?dist}
Summary:        Catppuccin GTK themes and icons collection
BuildArch:      noarch

License:        MIT
URL:            https://github.com/mecattaf/duoRPM
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

%description
Collection of Catppuccin GTK themes and icons for Sway/Wayland environments.
Includes Mocha and Noir variants of GTK themes and Catppuccin-SE icon set.

%prep
%setup -q

%install
# Install GTK themes
install -d %{buildroot}%{_datadir}/themes
cp -r themes/* %{buildroot}%{_datadir}/themes/

# Install icons
install -d %{buildroot}%{_datadir}/icons
cp -r icons/* %{buildroot}%{_datadir}/icons/

# Fix permissions for themes (directories 755, files 644)
find %{buildroot}%{_datadir}/themes -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/themes -type f -exec chmod 644 {} \;

# Fix permissions for icons (directories 755, files 644)
find %{buildroot}%{_datadir}/icons -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/icons -type f -exec chmod 644 {} \;

%files
%{_datadir}/themes/Catppuccin-Mocha-Standard-Green-Dark/
%{_datadir}/themes/Catppuccin-Noir-Standard-Green-Dark/
%{_datadir}/icons/Catppuccin-SE/
%{_datadir}/icons/default/

%changelog
* Fri Sep 27 2025 Mecattaf <thomas@mecattaf.dev> - 1.0.0-1
- Initial package with GTK themes and icons
