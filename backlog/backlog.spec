%global debug_package %{nil}

Name:           backlog
Version:        1.3.1
Release:        %autorelease
Summary:        Markdown-native Task Manager & Kanban visualizer for any Git repository

License:        MIT
URL:            https://github.com/MrLesk/Backlog.md
Source0:        %{url}/releases/download/v%{version}/backlog-bun-linux-x64
Source1:        %{url}/releases/download/v%{version}/backlog-bun-linux-arm64
Source2:        https://raw.githubusercontent.com/MrLesk/Backlog.md/v%{version}/README.md
Source3:        https://raw.githubusercontent.com/MrLesk/Backlog.md/v%{version}/LICENSE

# This is a prebuilt binary package
BuildArch:      noarch
ExclusiveArch:  x86_64 aarch64

Requires:       git-core
Requires:       glibc

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
# Install the appropriate binary based on architecture
%ifarch x86_64
install -Dpm755 %{SOURCE0} %{buildroot}%{_bindir}/backlog
%endif

%ifarch aarch64
install -Dpm755 %{SOURCE1} %{buildroot}%{_bindir}/backlog
%endif

# No shell completions are provided by backlog CLI

%files
%license LICENSE
%doc README.md
%{_bindir}/backlog

%changelog
%autochangelog
