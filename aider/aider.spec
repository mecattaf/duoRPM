Name:           aider
Version:        0.74.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

# Build requirements from pyproject.toml and compilation tools
BuildRequires:  python3-devel >= 3.9
BuildRequires:  python3-devel < 3.13
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools >= 68
BuildRequires:  python3-setuptools_scm >= 8
BuildRequires:  python3-setuptools_scm+toml >= 8
BuildRequires:  python3-wheel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  git-core
BuildRequires:  pkgconfig

# Runtime dependency for Python
Requires:       python3 >= 3.9
Requires:       python3 < 3.13

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
%autosetup -n %{name}-%{version}

%build
# Configure pip to use multiple indexes and find compatible wheels
export PIP_EXTRA_INDEX_URL="https://pypi.org/simple"
export PIP_FIND_LINKS="https://download.pytorch.org/whl/cpu"

# First install basic dependencies that don't need compilation
pip3 install --upgrade pip wheel setuptools
# Then install aider's requirements
PYTHONPATH="" pip3 install --no-deps --no-cache-dir -r requirements.txt || true
# Try to install any failed dependencies without version constraints
pip3 install --no-deps openai anthropic tiktoken rich prompt-toolkit pygments diskcache gitpython configargparse

# Build using pyproject.toml
python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir=%{buildroot} dist/*.whl

%files
%license LICENSE
%doc README.md
%{_bindir}/aider
%{python3_sitelib}/aider/
%{python3_sitelib}/aider_chat-*.dist-info/

%changelog
%autochangelog
