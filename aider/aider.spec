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
mkdir -p %{buildroot}/opt/aider
python3.12 -m venv %{buildroot}/opt/aider/venv

# Activate the venv and install aider
%{buildroot}/opt/aider/venv/bin/pip install --no-deps aider-chat==%{version}

# Create a wrapper script in /usr/bin
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/aider << 'EOF'
#!/bin/sh
exec /opt/aider/venv/bin/aider "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/aider

%files
/opt/aider/
%{_bindir}/aider

%changelog
%autochangelog
