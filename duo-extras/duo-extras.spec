%global debug_package %{nil}

Name:           duo-extras
Version:        1.0.0
Release:        1%{?dist}
Summary:        Catppuccin themes and icons for duo desktop environment

License:        MIT
URL:            https://github.com/mecattaf/zenRPM
Source0:        %{url}/releases/download/v%{version}/catppuccin-icons.tar.gz
Source1:        %{url}/releases/download/v%{version}/catppuccin-themes.tar.gz

BuildArch:      noarch

Requires:       gtk3
Recommends:     gtk4

%description
Custom Catppuccin themes and cursor icons for the duo desktop environment.
Includes Catppuccin-Mocha-Standard-Green-Dark and Catppuccin-Noir-Standard-Green-Dark
GTK themes, along with Catppuccin-SE cursor icons.

%prep
%setup -q -c -T
# Extract icons
tar -xf %{SOURCE0}
# Extract themes  
tar -xf %{SOURCE1}

%build
# Nothing to build for theme package

%install
# Install icons
mkdir -p %{buildroot}%{_datadir}/icons
if [ -d usr/share/icons ]; then
    cp -r usr/share/icons/* %{buildroot}%{_datadir}/icons/
elif [ -d icons ]; then
    cp -r icons/* %{buildroot}%{_datadir}/icons/
else
    # Handle different possible directory structures
    find . -type d -name "*catppuccin*" -o -name "*cursor*" | while read dir; do
        if [ -d "$dir" ] && [ "$(find "$dir" -name "cursors" -type d)" ]; then
            cp -r "$dir" %{buildroot}%{_datadir}/icons/
        fi
    done
fi

# Install themes
mkdir -p %{buildroot}%{_datadir}/themes
if [ -d usr/share/themes ]; then
    cp -r usr/share/themes/* %{buildroot}%{_datadir}/themes/
elif [ -d themes ]; then
    cp -r themes/* %{buildroot}%{_datadir}/themes/
else
    # Handle different possible directory structures
    find . -type d -name "*Catppuccin*" | while read dir; do
        if [ -d "$dir" ] && [ "$(find "$dir" -name "gtk-*" -type d)" ]; then
            cp -r "$dir" %{buildroot}%{_datadir}/themes/
        fi
    done
fi

# Set proper permissions
find %{buildroot}%{_datadir}/icons -type f -exec chmod 644 {} \;
find %{buildroot}%{_datadir}/icons -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/themes -type f -exec chmod 644 {} \;
find %{buildroot}%{_datadir}/themes -type d -exec chmod 755 {} \;

%files
%{_datadir}/icons/Catppuccin-SE/
%{_datadir}/icons/default/
%{_datadir}/themes/Catppuccin-Mocha-Standard-Green-Dark/
%{_datadir}/themes/Catppuccin-Noir-Standard-Green-Dark/

%changelog
* Mon Jun 09 2025 Thomas Mecattaf <thomas@mecattaf.dev> - 1.0.0-1
- Initial package for duo-extras themes and icons
