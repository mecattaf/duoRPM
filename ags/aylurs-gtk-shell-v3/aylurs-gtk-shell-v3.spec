# AGS v3 - Scaffolding CLI for Astal+Gnim
%global commit0 04d51ac4082af3ec47e8a803417a1a55b75151d7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 1

%bcond check 1

Name:           aylurs-gtk-shell-v3
Version:        3.0.0~%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        Scaffolding CLI for Astal+Gnim TypeScript projects

License:        GPL-3.0-only
URL:            https://github.com/Aylur/ags
Source0:        %{url}/archive/%{commit0}/ags-%{shortcommit0}.tar.gz

BuildRequires:  golang >= 1.21
BuildRequires:  git-core
BuildRequires:  pkgconfig(astal-gjs)
# astal-io no longer needed
BuildRequires:  pkgconfig(astal-3.0)
BuildRequires:  pkgconfig(astal-4-4.0)

# Runtime dependencies
Requires:       astal-gjs%{?_isa}
Requires:       astal-libs%{?_isa}
Requires:       astal%{?_isa}
Requires:       astal-gtk4%{?_isa}
# astal-io no longer needed
Requires:       gtk4-layer-shell%{?_isa} >= 1.2.0
Requires:       gjs%{?_isa}

# Node.js is needed for the TypeScript compilation at runtime
Requires:       nodejs >= 18
Requires:       npm

# Optional but recommended for full functionality
Recommends:     typescript
Recommends:     esbuild

# Conflicts with older versions
Conflicts:      aylurs-gtk-shell < 2.0
Conflicts:      aylurs-gtk-shell2 < %{version}
Obsoletes:      aylurs-gtk-shell2 < %{version}

# Provides for compatibility
Provides:       ags = %{version}-%{release}
Provides:       aylurs-gtk-shell = %{version}-%{release}

%description
AGS v3 is a scaffolding CLI tool for building desktop shells with Astal and Gnim.
It provides a TypeScript framework with JSX support for creating custom Wayland
desktop components using GTK3/GTK4 through GJS.

AGS v3 handles project initialization, bundling with esbuild, and provides
convenient APIs for working with Astal libraries.

%prep
%autosetup -n ags-%{commit0} -p1

%build
# Set up Go environment
export GO111MODULE=on
export GOPATH=%{_builddir}/gopath
export PATH=$GOPATH/bin:$PATH

# AGS v3 should be in the root or have a specific directory structure
# Check if there's a v3 directory
if [ -d v3 ]; then
    cd v3
fi

# Download Go dependencies
go mod download

# Build the AGS CLI with proper ldflags
go build -v -ldflags="-s -w \
    -X main.VERSION=%{version} \
    -X main.gtk4LayerShell=%{_libdir}/libgtk4-layer-shell.so.0 \
    -X main.astalGjs=%{_datadir}/astal/gjs" \
    -o ags ./cmd/ags || go build -v -ldflags="-s -w" -o ags .

%install
# Install the main binary
if [ -f v3/ags ]; then
    install -Dm755 v3/ags %{buildroot}%{_bindir}/ags
elif [ -f ags ]; then
    install -Dm755 ags %{buildroot}%{_bindir}/ags
else
    echo "Error: ags binary not found"
    exit 1
fi

# Generate and install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

%{buildroot}%{_bindir}/ags completion bash > %{buildroot}%{_datadir}/bash-completion/completions/ags
%{buildroot}%{_bindir}/ags completion fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/ags.fish
%{buildroot}%{_bindir}/ags completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_ags

# Install project templates if they exist
for dir in v3/templates templates; do
    if [ -d "$dir" ]; then
        mkdir -p %{buildroot}%{_datadir}/ags/templates
        cp -r "$dir"/* %{buildroot}%{_datadir}/ags/templates/
        break
    fi
done

%check
%if %{with check}
if [ -d v3 ]; then
    cd v3
fi
go test -v ./...
%endif

%files
%license LICENSE
%doc README.md
%doc docs/
%{_bindir}/ags
%{_datadir}/bash-completion/completions/ags
%{_datadir}/fish/vendor_completions.d/ags.fish
%{_datadir}/zsh/site-functions/_ags
%dir %{_datadir}/ags
# Templates may or may not exist
%{_datadir}/ags/

%changelog
* %{DATE} Your Name <your.email@example.com> - 3.0.0~1.git04d51ac-1
- Initial package of AGS v3
- Complete rewrite as Go-based scaffolding CLI
- Supports Astal+Gnim TypeScript projects
- astal-io has been deprecated and merged into core astal
