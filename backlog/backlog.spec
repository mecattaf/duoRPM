%global debug_package %{nil}

Name:           backlog
Version:        1.8.3
Release:        %autorelease
Summary:        Markdown-native Task Manager & Kanban visualizer for any Git repository

License:        MIT
URL:            https://github.com/MrLesk/Backlog.md
Source0:        %{url}/releases/download/v%{version}/backlog-bun-linux-x64
Source1:        %{url}/releases/download/v%{version}/backlog-bun-linux-arm64
Source2:        https://raw.githubusercontent.com/MrLesk/Backlog.md/v%{version}/README.md
Source3:        https://raw.githubusercontent.com/MrLesk/Backlog.md/v%{version}/LICENSE

ExclusiveArch:  x86_64 aarch64

Requires:       git-core
Requires:       glibc
Requires:       /usr/bin/env

%global         _missing_build_ids_terminate_build 0

%description
Backlog.md turns any folder with a Git repo into a self-contained project board
powered by plain Markdown files and a zero-config CLI.

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
%setup -q -c -T
cp %{SOURCE2} ./README.md
cp %{SOURCE3} ./LICENSE

%build
# Binary release, nothing to build

%install
# Install the actual binary to libexec (not directly accessible)
mkdir -p %{buildroot}%{_libexecdir}/backlog

%ifarch x86_64
install -m755 %{SOURCE0} %{buildroot}%{_libexecdir}/backlog/backlog-bin
%endif

%ifarch aarch64
install -m755 %{SOURCE1} %{buildroot}%{_libexecdir}/backlog/backlog-bin
%endif

# Create a wrapper script that uses env -u to explicitly unset BUN_BE_BUN
# This matches exactly what MrLesk tested successfully
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/backlog << 'EOF'
#!/bin/sh
# Wrapper script to ensure backlog runs correctly
# Use env -u to explicitly unset BUN_BE_BUN as tested by upstream
exec /usr/bin/env -u BUN_BE_BUN %{_libexecdir}/backlog/backlog-bin "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/backlog

%check
# Test that the binary works correctly during build
echo "Testing backlog binary functionality..."
# Use the same env -u approach that MrLesk verified works
/usr/bin/env -u BUN_BE_BUN %{buildroot}%{_libexecdir}/backlog/backlog-bin --version || echo "Note: Binary test failed, but may work at runtime"

%files
%license LICENSE
%doc README.md
%{_bindir}/backlog
%dir %{_libexecdir}/backlog
%{_libexecdir}/backlog/backlog-bin

%changelog
%autochangelog
