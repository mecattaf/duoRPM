Name:           aider
Version:        0.74.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

# Minimal build requirements
BuildRequires:  python3-devel >= 3.12
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

# Runtime dependency just for Python 3.12
Requires:       python3 >= 3.12

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
%autosetup -n %{name}-%{version}

%build
# Install all dependencies from requirements.txt
pip3 install --no-deps -r requirements.txt
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
