Name:           aider
Version:        0.74.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider

BuildArch:      noarch

BuildRequires:  python3.12
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

# Runtime dependency for Python
Requires:       python3.12

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
# Nothing to prep

%build
# Nothing to build

%install
# Ensure pip is available for Python 3.12
python3.12 -m ensurepip
python3.12 -m pip install --upgrade pip

# Install directly from PyPI
python3.12 -m pip install --no-deps --root %{buildroot} aider-chat==%{version}

%files
%{python3_sitelib}/aider/
%{python3_sitelib}/aider_chat-*.dist-info/
%{_bindir}/aider

%changelog
%autochangelog
