Name:           aider
Version:        0.74.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.9
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

# Runtime dependency for Python
Requires:       python3 >= 3.9

%description
Aider is a terminal-based coding assistant that lets you program with 
LLM models like GPT-4 or Claude. It helps maintain conversation context
and can directly edit code files based on the AI's suggestions.

%prep
# Nothing to prep

%build
# Nothing to build

%install
# Install directly from PyPI
pip3 install --no-deps --root %{buildroot} aider-chat==%{version}

%files
%{python3_sitelib}/aider/
%{python3_sitelib}/aider_chat-*.dist-info/
%{_bindir}/aider

%changelog
%autochangelog
