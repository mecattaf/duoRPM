Name:           aider
Version:        0.20.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

# Runtime dependencies - from requirements.txt but without version locks
# to use Fedora's package versions
%generate_buildrequires
%pyproject_buildrequires

Requires:       python3 >= 3.9
Requires:       python3 < 3.13
# Core dependencies from requirements.txt
Requires:       (python3dist(openai) >= 1.0.0 or python3-openai >= 1.0.0)
Requires:       (python3dist(anthropic) >= 0.18.1 or python3-anthropic >= 0.18.1)
Requires:       (python3dist(tokenizers) or python3-tokenizers)
Requires:       (python3dist(prompt-toolkit) or python3-prompt-toolkit)
Requires:       (python3dist(pygments) or python3-pygments)
Requires:       (python3dist(rich) or python3-rich)
Requires:       (python3dist(diskcache) or python3-diskcache)
Requires:       (python3dist(gitpython) or python3-gitpython)
Requires:       (python3dist(tiktoken) or python3-tiktoken)

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
%autosetup -n %{name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files aider

%files -n %{name}
%license LICENSE
%doc README.md
%{_bindir}/aider
%{python3_sitelib}/aider/
%{python3_sitelib}/aider-*.egg-info/

%changelog
%autochangelog
