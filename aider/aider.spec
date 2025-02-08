Name:           aider
Version:        0.20.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.12
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
# Additional build requirements from the error log
BuildRequires:  python3-annotated-types
BuildRequires:  python3-anyio
BuildRequires:  python3-attrs
BuildRequires:  python3-backoff
BuildRequires:  python3-certifi
BuildRequires:  python3-cffi
BuildRequires:  python3-charset-normalizer
BuildRequires:  python3-configargparse
BuildRequires:  python3-diskcache
BuildRequires:  python3-gitdb
BuildRequires:  python3-httpcore
BuildRequires:  python3-httpx
BuildRequires:  python3-markdown-it
BuildRequires:  python3-networkx
BuildRequires:  python3-numpy
BuildRequires:  python3-openai
BuildRequires:  python3-packaging
BuildRequires:  python3-pillow
BuildRequires:  python3-prompt-toolkit
BuildRequires:  python3-pydantic
BuildRequires:  python3-pygments
BuildRequires:  python3-pyyaml
BuildRequires:  python3-requests
BuildRequires:  python3-rich
BuildRequires:  python3-scipy
BuildRequires:  python3-tqdm
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-urllib3

Requires:       python3 >= 3.12
# Core runtime dependencies
Requires:       python3-openai
Requires:       python3-anthropic
Requires:       python3-tokenizers
Requires:       python3-prompt-toolkit
Requires:       python3-pygments
Requires:       python3-rich
Requires:       python3-diskcache
Requires:       python3-gitpython
Requires:       python3-tiktoken
Requires:       python3-configargparse

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{_bindir}/aider
%{python3_sitelib}/aider/
%{python3_sitelib}/aider-*.egg-info/

%changelog
%autochangelog
