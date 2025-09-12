# ========================================
# astal-gjs.spec - GJS bindings (JavaScript)
# ========================================
%global astal_commit 344a6dce56437a190b99e516a6cab8332cccf19e
%global astal_shortcommit %(c=%{astal_commit}; echo ${c:0:7})
%global bumpver 4

%global debug_package %{nil}
%global _vpath_srcdir lang/gjs

Name:           astal-gjs
Version:        0.1.0~%{bumpver}.git%{astal_shortcommit}
Release:        %autorelease
Summary:        GJS/JavaScript bindings for Astal

License:        LGPL-2.1-only
URL:            https://github.com/Aylur/astal
Source0:        %{url}/archive/%{astal_commit}/astal-%{astal_shortcommit}.tar.gz

BuildRequires:  meson >= 0.59.0
BuildRequires:  pkgconfig(astal-3.0)
BuildRequires:  pkgconfig(astal-4-4.0)
# astal-io no longer needed

Requires:       gjs%{?_isa}
# Remove version locks to avoid circular deps
Requires:       astal%{?_isa}
Requires:       astal-gtk4%{?_isa}

Supplements:    astal

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for %{name}.

%description
GJS/JavaScript bindings for the Astal desktop shell framework, enabling
JavaScript developers to create desktop shells using Astal libraries.

%prep
%autosetup -n astal-%{astal_commit} -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%dir %{_datadir}/astal
%{_datadir}/astal/gjs/

%files devel
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
