Name:           whisper-transcription
Version:        1.0.0
Release:        %autorelease
Summary:        Speech-to-text transcription tool for Wayland

License:        GPL-3.0-only
URL:            https://github.com/mecattaf/whisper-transcription-wayland
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  rust-packaging
BuildRequires:  pkg-config
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel

%description
A speech-to-text transcription tool for Wayland that records audio and
converts it to text using the Whisper model.

%prep
%autosetup
%{__cargo} vendor
mkdir -p .cargo
cat > .cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%{__cargo} build --release

%install
mkdir -p %{buildroot}%{_bindir}
install -Dpm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog
