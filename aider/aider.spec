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
mkdir -p %{buildroot}%{_libdir}/aider
python3.12 -m venv %{buildroot}%{_libdir}/aider/venv

# Install aider in the venv
%{buildroot}%{_libdir}/aider/venv/bin/pip install --no-deps aider-chat==%{version}

# Remove absolute buildroot paths from pyvenv.cfg to avoid check-buildroot errors
sed -i "s|%{buildroot}||g" %{buildroot}%{_libdir}/aider/venv/pyvenv.cfg

# Create bindir and symlink the venv's aider binary
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/aider/venv/bin/aider %{buildroot}%{_bindir}/aider

%files
%dir %{_libdir}/aider
%{_libdir}/aider/venv/bin/aider
%attr(755,root,root) %{_bindir}/aider

%changelog
%autochangelog
