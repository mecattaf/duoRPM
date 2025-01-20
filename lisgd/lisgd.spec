Name:           lisgd
Version:        0.4.0
Release:        %autorelease
Summary:        Libinput synthetic gesture daemon for touchscreens

License:        MIT
URL:            https://git.sr.ht/~mil/lisgd
Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libinput-devel
BuildRequires:  systemd-devel
BuildRequires:  libX11-devel
BuildRequires:  wayland-devel

%description
Lisgd (libinput synthetic gesture daemon) lets you bind gestures based on
libinput touch events to run specific commands to execute. For example, dragging
left to right with one finger could execute a particular command like launching
a terminal. Directional L-R, R-L, U-D, and D-U gestures and diagnoal LD-RU,
RD-LU, UR-DL, UL-DR gestures are supported with 1 through n fingers.

%prep
%autosetup

%build
%make_build

%install
install -m 755 -D lisgd "%{buildroot}%{_bindir}/lisgd"
install -m 644 -D lisgd.1 "%{buildroot}%{_mandir}/man1/lisgd.1"

%files
%{_bindir}/lisgd
%{_mandir}/man1/lisgd.1.*
%license LICENSE
%doc README.md

%changelog
%autochangelog
