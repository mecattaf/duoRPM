%global debug_package %{nil}

Name:           backlog-test
Version:        1.8.3
Release:        %autorelease
Summary:        Markdown-native Task Manager & Kanban visualizer (built from source)

License:        MIT
URL:            https://github.com/MrLesk/Backlog.md
Source0:        https://github.com/MrLesk/Backlog.md/archive/v%{version}/Backlog.md-%{version}.tar.gz

BuildRequires:  curl
BuildRequires:  git-core
BuildRequires:  gcc-c++
BuildRequires:  libstdc++-devel
BuildRequires:  glibc-devel

# We'll install bun during build since it's not in Fedora repos
BuildArch:      x86_64 aarch64

Requires:       git-core
Requires:       glibc
Requires:       libstdc++

# Conflicts with the prebuilt package
Conflicts:      backlog

%description
Backlog.md turns any folder with a Git repo into a self-contained project board
powered by plain Markdown files and a zero-config CLI.

This package builds backlog from source using Bun, avoiding the BUN_BE_BUN issue
present in the prebuilt binaries.

Features:
- Markdown-native tasks - manage every issue as a plain .md file
- 100%% private & offline - backlog lives entirely inside your repo
- Instant terminal Kanban - backlog board paints a live board in your shell
- Board export - backlog board export creates shareable markdown reports
- Modern web interface - backlog browser launches a sleek web UI
- AI-ready CLI - "Claude, please take over task 33"
- Rich query commands - view, list, filter, or archive tasks with ease
- MIT-licensed & open-source - free for personal or commercial use

%prep
%autosetup -n Backlog.md-%{version}

%build
# Install Bun in the build environment
export BUN_INSTALL="$HOME/.bun"
curl -fsSL https://bun.sh/install | bash
export PATH="$BUN_INSTALL/bin:$PATH"

# Verify Bun installation
bun --version

# Disable Husky git hooks that are failing in the build environment
export HUSKY=0
export CI=true

# Install dependencies (production only)
# The --ignore-scripts flag will also prevent husky from running
bun install --production --frozen-lockfile --ignore-scripts

# Build CSS first (required step from their build process)
bun run build:css

# Build the standalone executable with embedded version
# Using flags from Perplexity guide and matching what backlog does in flake.nix
bun build --compile --minify --sourcemap --bytecode \
    --define "__EMBEDDED_VERSION__=%{version}" \
    --outfile=backlog \
    src/cli.ts

# Verify the binary works correctly (should show backlog version, not Bun)
./backlog --version | grep -q "%{version}" || (echo "ERROR: Binary shows wrong version" && exit 1)
./backlog --help | head -1 | grep -q "backlog" || (echo "ERROR: Binary shows Bun help instead of backlog" && exit 1)

# Strip debug symbols to reduce size
strip backlog || true

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 backlog %{buildroot}%{_bindir}/backlog

%check
# Additional verification that the installed binary works
%{buildroot}%{_bindir}/backlog --version | grep -q "%{version}"
%{buildroot}%{_bindir}/backlog --help | grep -q "backlog"

%files
%license LICENSE
%doc README.md
%{_bindir}/backlog

%changelog
%autochangelog
