Name:           aider
Version:        0.74.0
Release:        %autorelease
Summary:        Command-line AI coding assistant

License:        MIT
URL:            https://github.com/paul-gauthier/aider
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

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
%autosetup -n %{name}-%{version}

%build
# Nothing to build

%install
# Install directly with pip into the correct location
pip3 install --no-deps --root %{buildroot} .

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/aider/
%{python3_sitelib}/aider_chat-*.dist-info/
%{_bindir}/aider

%changelog
%autochangelog
