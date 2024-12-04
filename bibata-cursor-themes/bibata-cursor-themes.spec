%global         source_name Bibata_Cursor
%global         debug_package %{nil}

Name:           bibata-cursor-themes
Version:        2.0.7
Release:        1%{?dist}
Summary:        OpenSource, Compact and Material Designed Cursor Set

License:        GNU General Public License v3.0
URL:            https://github.com/ful1e5/Bibata_Cursor
Source:         %{url}/archive/v%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/bitmaps.zip

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-pip

Requires:       gtk3

%description
OpenSource, Compact and Material Designed Cursor Set

%prep
%autosetup -c
%autosetup -T -D -a 1

mv bitmaps %{source_name}-%{version}

%build
export PATH="/builddir/.local/bin:$PATH"
pip install clickgen

cd %{source_name}-%{version}

declare -A normal_names
normal_names["Bibata-Modern-Amber"]="Yellowish and rounded edge Bibata cursors"
normal_names["Bibata-Modern-Classic"]="Black and rounded edge Bibata cursors"
normal_names["Bibata-Modern-Ice"]="White and rounded edge Bibata cursors"
normal_names["Bibata-Original-Amber"]="Yellowish and sharp edge Bibata cursors"
normal_names["Bibata-Original-Classic"]="Black and sharp edge Bibata cursors"
normal_names["Bibata-Original-Ice"]="White and sharp edge Bibata cursors"

for key in "${!normal_names[@]}"; do
    comment="${normal_names[$key]}"
    ctgen configs/normal/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "$comment"
done

declare -A right_names
right_names["Bibata-Modern-Amber-Right"]="Yellowish and rounded edge right-hand Bibata cursors"
right_names["Bibata-Modern-Classic-Right"]="Black and rounded edge right-hand Bibata cursors"
right_names["Bibata-Modern-Ice-Right"]="White and rounded edge right-hand Bibata cursors"
right_names["Bibata-Original-Amber-Right"]="Yellowish and sharp edge right-hand Bibata cursors"
right_names["Bibata-Original-Classic-Right"]="Black and sharp edge right-hand Bibata cursors"
right_names["Bibata-Original-Ice-Right"]="White and sharp edge right-hand Bibata cursors"

for key in "${!right_names[@]}"; do
    comment="${right_names[$key]}"
    ctgen configs/right/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "$comment"
done

%install
%__rm -rf %{buildroot}
%__mkdir -p %{buildroot}%{_datadir}/icons
for theme in $(ls %{_builddir}/%{name}-%{version}/%{source_name}-%{version}/themes); do
    %__mv %{_builddir}/%{name}-%{version}/%{source_name}-%{version}/themes/${theme} %{buildroot}%{_datadir}/icons
    %__chmod 0755 %{buildroot}%{_datadir}/icons/${theme}
done

%clean
%__rm -rf %{buildroot}

%files
%license %{source_name}-%{version}/LICENSE
%doc %{source_name}-%{version}/README.md
%{_datadir}/icons/*

%changelog
* Tue 18 Jun 2024 02:07:00 PM EDT
- New Release - v2.0.7

* Thu 25 Jan 2024 09:21:25 PST
- New Release - v2.0.6

* Sun 31 Dec 2023 09:51:50 AM EST
- New Release - v2.0.5

* Sat 16 Dec 2023 05:38:01 PM EST
- New Release - v2.0.4

* Tue 06 Dec 2022 09:17:20 AM EST
- New Release - v2.0.3

* Mon Oct 10 09:56:59 AM EDT 2022
- New Release - v2.0.2

* Thu Oct 06 09:27:08 EDT 2022 Peter Wu
- New Release - v2.0.1

* Mon Oct  3 12:07:28 EDT 2022 Peter Wu
- New Release - v2.0.0

* Sun 05 Jun 2022 07:54:12 PM EDT Peter Wu
- Use bitmaps.zip to build

* Mon Jul 12 09:44:23 AM EDT 2021 Peter Wu
- New Release - v1.1.2

* Fri Mar 26 09:52:42 AM EDT 2021 Peter Wu
- New Release - v1.1.1

* Fri Feb 26 09:45:42 EST 2021 Peter Wu
- New Release - v1.1.0

* Tue Nov 17 09:42:13 EST 2020 Peter Wu <peterwu@hotmail.com>
- New Release - v1.0.3
