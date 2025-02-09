Name:           aider
Version:        0.74.0
Release:        2%{?dist}
Summary:        Command-line AI coding assistant tool

License:        MIT
URL:            https://github.com/paul-gauthier/aider

BuildRequires:  python3.12
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  chrpath

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
# Create the directory for aider under the Python library directory.
mkdir -p %{buildroot}%{_libdir}/aider

# Create a Python virtual environment for aider.
python3.12 -m venv %{buildroot}%{_libdir}/aider/venv

# Install aider-chat into the virtual environment.
%{buildroot}%{_libdir}/aider/venv/bin/pip install aider-chat==%{version}

# Remove buildroot references from the venv’s text files.
find %{buildroot}%{_libdir}/aider/venv/bin -type f -exec sed -i "s|%{buildroot}||g" {} +
sed -i "s|%{buildroot}||g" %{buildroot}%{_libdir}/aider/venv/pyvenv.cfg

# Fix Python shebangs in all scripts inside the virtual environment.
find %{buildroot}%{_libdir}/aider/venv -type f -exec sed -i 's|#!/usr/bin/env python$|#!/usr/bin/python3|' {} +

# Remove invalid RPATH entries from compiled modules.
find %{buildroot}%{_libdir}/aider/venv -type f -name "*.so" -exec chrpath --delete {} \;

# Create the binary directory and a relative symlink for the aider executable.
mkdir -p %{buildroot}%{_bindir}
ln -rs %{_libdir}/aider/venv/bin/aider %{buildroot}%{_bindir}/aider

%files
%dir %{_libdir}/aider
%{_libdir}/aider/venv
%{_bindir}/aider

%changelog
%autochangelog
