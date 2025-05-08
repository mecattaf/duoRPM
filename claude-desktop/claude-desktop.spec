%global debug_package %{nil}

# Source URL for the Claude Desktop Windows installer
%global source_url https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-x64/Claude-Setup-x64.exe

Name:           claude-desktop
Version:        0.7.7
Release:        %autorelease
Summary:        Desktop application for Claude AI by Anthropic

License:        Proprietary
URL:            https://www.anthropic.com
Source0:        %{source_url}
Source1:        https://raw.githubusercontent.com/bsneed/claude-desktop-fedora/main/build-fedora.sh
Source2:        https://raw.githubusercontent.com/bsneed/claude-desktop-fedora/main/LICENSE-MIT
Source3:        https://raw.githubusercontent.com/bsneed/claude-desktop-fedora/main/LICENSE-APACHE

# For dependencies, based on requirements in build-fedora.sh
BuildRequires:  p7zip-plugins
BuildRequires:  wget
BuildRequires:  icoutils
BuildRequires:  ImageMagick
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  desktop-file-utils

# Electron and runtime requirements
Requires:       nodejs
Requires:       electron
Requires:       p7zip-plugins

ExclusiveArch:  x86_64

%description
Claude Desktop is the official desktop application for Claude AI by Anthropic.
This package provides a Linux-compatible version of the official Windows desktop
application, modified to work on Fedora-based systems.

Features include:
- Native desktop experience for Claude AI
- Fast access via global keyboard shortcut (Ctrl+Alt+Space)
- System tray integration
- Full Claude functionality including file uploads and Claude Pro features

Note: This is an unofficial build script; not officially supported by Anthropic.

%prep
# Create work directory
mkdir -p %{_builddir}/claude-desktop-build

# Download the build script for reference
cp %{SOURCE1} %{_builddir}/claude-desktop-build/build-fedora.sh
cp %{SOURCE2} %{_builddir}/claude-desktop-build/LICENSE-MIT
cp %{SOURCE3} %{_builddir}/claude-desktop-build/LICENSE-APACHE

# Extract the Windows installer
cd %{_builddir}/claude-desktop-build
7z x -y %{SOURCE0}

# Find the nupkg file
NUPKG_FILE=$(find . -name "AnthropicClaude-*-full.nupkg" | head -1)
if [ -z "$NUPKG_FILE" ]; then
    echo "Could not find AnthropicClaude nupkg file"
    exit 1
fi

# Extract the nupkg
7z x -y "$NUPKG_FILE"

# Extract icons
wrestool -x -t 14 "lib/net45/claude.exe" -o claude.ico
icotool -x claude.ico

%build
cd %{_builddir}/claude-desktop-build

# Map icon sizes to their corresponding extracted files
declare -A icon_files=(
    ["16"]="claude_13_16x16x32.png"
    ["24"]="claude_11_24x24x32.png"
    ["32"]="claude_10_32x32x32.png"
    ["48"]="claude_8_48x48x32.png"
    ["64"]="claude_7_64x64x32.png"
    ["256"]="claude_6_256x256x32.png"
)

# Process app.asar
mkdir -p electron-app
cp "lib/net45/resources/app.asar" electron-app/
cp -r "lib/net45/resources/app.asar.unpacked" electron-app/

cd electron-app
npx asar extract app.asar app.asar.contents || { echo "asar extract failed"; exit 1; }

# Attempt to modify window frame settings
sed -i 's/height:e\.height,titleBarStyle:"default",titleBarOverlay:[^,]\+,/height:e.height,frame:true,/g' app.asar.contents/.vite/build/index.js || echo "Warning: sed command failed to modify index.js"

# Create stub native module
mkdir -p app.asar.contents/node_modules/claude-native
cat > app.asar.contents/node_modules/claude-native/index.js << EOF
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
cp ../lib/net45/resources/Tray* app.asar.contents/resources/

# Repackage app.asar
mkdir -p app.asar.contents/resources/i18n/
cp ../lib/net45/resources/*.json app.asar.contents/resources/i18n/

# Add main window fix from emsi's repository
curl -sL https://github.com/emsi/claude-desktop/raw/main/assets/main_window.tgz | tar -zxvf - -C app.asar.contents/

# Pack the asar file
npx asar pack app.asar.contents app.asar || { echo "asar pack failed"; exit 1; }

%install
cd %{_builddir}/claude-desktop-build

# Create directory structure
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons

# Install app.asar and app.asar.unpacked
cp electron-app/app.asar %{buildroot}%{_libdir}/%{name}/

# Create native module directory structure
mkdir -p %{buildroot}%{_libdir}/%{name}/app.asar.unpacked/node_modules/claude-native
cat > %{buildroot}%{_libdir}/%{name}/app.asar.unpacked/node_modules/claude-native/index.js << EOF
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

# Install icons
for size in 16 24 32 48 64 256; do
    icon_dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
    mkdir -p "${icon_dir}"
    if [ -f "${icon_files[$size]}" ]; then
        install -Dm 644 "${icon_files[$size]}" "${icon_dir}/claude-desktop.png"
    fi
done

# Install desktop entry
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Claude
Exec=claude-desktop %u
Icon=claude-desktop
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
electron %{_libdir}/%{name}/app.asar --ozone-platform-hint=auto --enable-logging=file --log-file=\$LOG_FILE --log-level=INFO "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
# Update icon caches
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor || :
# Force icon theme cache rebuild
touch -h %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications || :

# Set correct permissions for chrome-sandbox
echo "Setting chrome-sandbox permissions..."
SANDBOX_PATH=""

# Check for sandbox in system-installed electron
if command -v electron >/dev/null 2>&1; then
    ELECTRON_PATH=$(command -v electron)
    ELECTRON_ROOT=$(dirname $(dirname $ELECTRON_PATH))
    
    # Check common locations for electron's chrome-sandbox
    for potential_path in \
        "$ELECTRON_ROOT/lib/electron/chrome-sandbox" \
        "$ELECTRON_ROOT/lib64/electron/chrome-sandbox" \
        "$ELECTRON_ROOT/lib/node_modules/electron/dist/chrome-sandbox" \
        "$ELECTRON_ROOT/lib64/node_modules/electron/dist/chrome-sandbox" \
        "/usr/lib/electron/chrome-sandbox" \
        "/usr/lib64/electron/chrome-sandbox" \
        "/usr/lib/node_modules/electron/dist/chrome-sandbox" \
        "/usr/lib64/node_modules/electron/dist/chrome-sandbox"; do
        
        if [ -f "$potential_path" ]; then
            SANDBOX_PATH="$potential_path"
            break
        fi
    done
fi

if [ -n "$SANDBOX_PATH" ] && [ -f "$SANDBOX_PATH" ]; then
    echo "Found chrome-sandbox at: $SANDBOX_PATH"
    chown root:root "$SANDBOX_PATH" || echo "Warning: Failed to chown chrome-sandbox"
    chmod 4755 "$SANDBOX_PATH" || echo "Warning: Failed to chmod chrome-sandbox"
    echo "Permissions set for $SANDBOX_PATH"
else
    echo "Warning: chrome-sandbox binary not found. Sandbox may not function correctly."
fi

%files
%license %{_builddir}/claude-desktop-build/LICENSE-MIT
%license %{_builddir}/claude-desktop-build/LICENSE-APACHE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/claude-desktop.png

%changelog
* Wed May 08 2025 Package Maintainer <maintainer@example.com> - 0.7.7-1
- Initial package
