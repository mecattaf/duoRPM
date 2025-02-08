Name:           aider
Version:        0.74.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

# Build dependencies
BuildRequires:  python3-devel >= 3.9
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pipx
BuildRequires:  git-core

# Runtime dependencies
Requires:       python3 >= 3.9
Requires:       pipx

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build - using pipx for installation

%install
# Create directories for pipx
export PIPX_HOME=%{buildroot}%{_prefix}/lib/pipx
export PIPX_BIN_DIR=%{buildroot}%{_bindir}
mkdir -p $PIPX_HOME $PIPX_BIN_DIR

# Install aider using pipx
pipx install . \
    --python %{python3} \
    --include-deps \
    --verbose

%files
%license LICENSE
%doc README.md
%{_bindir}/aider
%{_prefix}/lib/pipx/venvs/aider*
%{_prefix}/lib/pipx/venvs/.local/pipx/venvs/aider*

%changelog
%autochangelog
