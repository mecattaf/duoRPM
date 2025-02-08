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
# Create a venv directory in the package
mkdir -p %{buildroot}%{_exec_prefix}/lib/aider
python3.12 -m venv %{buildroot}%{_exec_prefix}/lib/aider/venv

# Install aider in the venv
%{buildroot}%{_exec_prefix}/lib/aider/venv/bin/pip install --no-deps aider-chat==%{version}

# Create bindir and symlink the venv's aider binary
mkdir -p %{buildroot}%{_bindir}
ln -s %{_exec_prefix}/lib/aider/venv/bin/aider %{buildroot}%{_bindir}/aider

%files
%dir %{_exec_prefix}/lib/aider
%{_exec_prefix}/lib/aider/venv/
%{_bindir}/aider

%changelog
%autochangelog
