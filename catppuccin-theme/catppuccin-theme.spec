Name:           catppuccin-theme
Version:        1.0.0
Release:        1%{?dist}
Summary:        Catppuccin themes and icons for GTK environments

License:        GPL-3.0
URL:            https://github.com/mecattaf/catppuccin-theme
Source0:        %{url}/releases/download/v%{version}/catppuccin-theme.tar.gz

BuildArch:      noarch

%description
Catppuccin themes and icons offering a cozy and warm color scheme 
for GTK environments.

%prep
%autosetup

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}

# Extract the tar.gz file directly into the buildroot.
tar -xzf %{SOURCE0} -C %{buildroot}%{_datadir}

# Move the icons and themes to the expected locations.
mv %{buildroot}%{_datadir}/catppuccin-theme/icons %{buildroot}%{_datadir}
mv %{buildroot}%{_datadir}/catppuccin-theme/themes %{buildroot}%{_datadir}

%files
%{_datadir}/icons/*
%{_datadir}/themes/*

%changelog
* Wed Dec 04 2024 Maintainer <thomasmecattaf@gmail.com> - 1.0.0
- Initial release using GitHub releases
