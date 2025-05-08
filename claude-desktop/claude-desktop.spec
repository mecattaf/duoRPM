%global debug_package %{nil}

# Source URL for the Claude Desktop Windows installer
%global source_url https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-x64/Claude-Setup-x64.exe
# Source URL for Electron
%global electron_url https://github.com/electron/electron/releases/download/v28.2.0/electron-v28.2.0-linux-x64.zip

Name:           claude-desktop
Version:        0.7.7
Release:        %autorelease
Summary:        Desktop application for Claude AI by Anthropic

License:        MIT AND Apache-2.0
URL:            https://github.com/bsneed/claude-desktop-fedora
Source0:        %{source_url}
Source1:        %{electron_url}
Source2:        LICENSE-MIT
Source3:        LICENSE-APACHE

# For dependencies
BuildRequires:  p7zip-plugins
BuildRequires:  wget
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  desktop-file-utils
BuildRequires:  unzip

# Runtime requirements
Requires:       nodejs
Requires:       p7zip-plugins

ExclusiveArch:  x86_64

%description
Claude Desktop is the official desktop application for Claude AI by Anthropic.
This package provides a Linux-compatible version of the official Windows desktop
application, modified to work on Fedora-based systems.

This is an unofficial adaptation and is not officially supported by Anthropic.
The build scripts are dual-licensed under MIT and Apache 2.0, while the Claude 
Desktop application itself is proprietary software from Anthropic.

%prep
# Create work directory
mkdir -p %{_builddir}/%{name}-build

# Copy license files
cp %{SOURCE2} %{_builddir}/%{name}-build/LICENSE-MIT
cp %{SOURCE3} %{_builddir}/%{name}-build/LICENSE-APACHE

# Download Electron for bundling
cd %{_builddir}/%{name}-build
wget -c %{electron_url} -O electron.zip
unzip electron.zip -d electron

# Download the Windows installer
wget -c %{source_url} -O Claude-Setup-x64.exe

# Extract the Windows installer
7z x -y Claude-Setup-x64.exe

# Find the nupkg file
NUPKG_FILE=$(find . -name "AnthropicClaude-*-full.nupkg" | head -1)
if [ -z "$NUPKG_FILE" ]; then
    echo "Could not find AnthropicClaude nupkg file"
    exit 1
fi

# Extract the nupkg
7z x -y "$NUPKG_FILE"

%build
cd %{_builddir}/%{name}-build

# Process app.asar
mkdir -p electron-app
cp "lib/net45/resources/app.asar" electron-app/
cp -r "lib/net45/resources/app.asar.unpacked" electron-app/ || true

cd electron-app
npx asar extract app.asar app.asar.contents || { echo "asar extract failed"; exit 1; }

# Attempt to modify window frame settings
sed -i 's/height:e\.height,titleBarStyle:"default",titleBarOverlay:[^,]\+,/height:e.height,frame:true,/g' app.asar.contents/.vite/build/index.js || echo "Warning: sed command failed to modify index.js"

# Create stub native module
mkdir -p app.asar.contents/node_modules/claude-native
cat > app.asar.contents/node_modules/claude-native/index.js << 'EOF'
// Stub implementation of claude-native using KeyboardKey enum values
const KeyboardKey = {
  Backspace: 43,
  Tab: 280,
  Enter: 261,
  Shift: 272,
  Control: 61,
  Alt: 40,
  CapsLock: 56,
  Escape: 85,
  Space: 276,
  PageUp: 251,
  PageDown: 250,
  End: 83,
  Home: 154,
  LeftArrow: 175,
  UpArrow: 282,
  RightArrow: 262,
  DownArrow: 81,
  Delete: 79,
  Meta: 187
};

Object.freeze(KeyboardKey);

module.exports = {
  getWindowsVersion: () => "10.0.0",
  setWindowEffect: () => {},
  removeWindowEffect: () => {},
  getIsMaximized: () => false,
  flashFrame: () => {},
  clearFlashFrame: () => {},
  showNotification: () => {},
  setProgressBar: () => {},
  clearProgressBar: () => {},
  setOverlayIcon: () => {},
  clearOverlayIcon: () => {},
  KeyboardKey
};
EOF

# Copy Tray icons
mkdir -p app.asar.contents/resources
cp -f ../lib/net45/resources/Tray* app.asar.contents/resources/ || true

# Repackage app.asar
mkdir -p app.asar.contents/resources/i18n/
cp -f ../lib/net45/resources/*.json app.asar.contents/resources/i18n/ || true

# Add main window fix from emsi's repository
curl -sL https://github.com/emsi/claude-desktop/raw/main/assets/main_window.tgz | tar -zxvf - -C app.asar.contents/ || echo "Warning: Failed to add main window fix"

# Pack the asar file
npx asar pack app.asar.contents app.asar || { echo "asar pack failed"; exit 1; }

%install
cd %{_builddir}/%{name}-build

# Create directory structure
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}

# Install app.asar
cp electron-app/app.asar %{buildroot}%{_libdir}/%{name}/

# Install bundled electron
cp -r electron/* %{buildroot}%{_libdir}/%{name}/

# Create native module directory structure
mkdir -p %{buildroot}%{_libdir}/%{name}/app.asar.unpacked/node_modules/claude-native
cat > %{buildroot}%{_libdir}/%{name}/app.asar.unpacked/node_modules/claude-native/index.js << 'EOF'
// Stub implementation of claude-native using KeyboardKey enum values
const KeyboardKey = {
  Backspace: 43,
  Tab: 280,
  Enter: 261,
  Shift: 272,
  Control: 61,
  Alt: 40,
  CapsLock: 56,
  Escape: 85,
  Space: 276,
  PageUp: 251,
  PageDown: 250,
  End: 83,
  Home: 154,
  LeftArrow: 175,
  UpArrow: 282,
  RightArrow: 262,
  DownArrow: 81,
  Delete: 79,
  Meta: 187
};

Object.freeze(KeyboardKey);

module.exports = {
  getWindowsVersion: () => "10.0.0",
  setWindowEffect: () => {},
  removeWindowEffect: () => {},
  getIsMaximized: () => false,
  flashFrame: () => {},
  clearFlashFrame: () => {},
  showNotification: () => {},
  setProgressBar: () => {},
  clearProgressBar: () => {},
  setOverlayIcon: () => {},
  clearOverlayIcon: () => {},
  KeyboardKey
};
EOF

# Install license files
install -m 644 LICENSE-MIT %{buildroot}%{_datadir}/licenses/%{name}/
install -m 644 LICENSE-APACHE %{buildroot}%{_datadir}/licenses/%{name}/

# Install desktop entry (without icon reference)
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Claude
Exec=claude-desktop %u
Type=Application
Terminal=false
Categories=Office;Utility;
MimeType=x-scheme-handler/claude;
StartupWMClass=claude
EOF

# Install launcher script
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
LOG_FILE="\$HOME/claude-desktop-launcher.log"
%{_libdir}/%{name}/electron %{_libdir}/%{name}/app.asar --ozone-platform-hint=auto --enable-logging=file --log-file=\$LOG_FILE --log-level=INFO "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
# Update desktop database
update-desktop-database %{_datadir}/applications || :

%files
%license %{_datadir}/licenses/%{name}/LICENSE-MIT
%license %{_datadir}/licenses/%{name}/LICENSE-APACHE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed May 08 2024 Package Maintainer <maintainer@example.com> - 0.7.7-1
- Update to bundle Electron with the package
- Remove dependency on external electron package
- Initial package for Claude Desktop on Fedora
