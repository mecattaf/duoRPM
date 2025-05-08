# Fedora package documentation for Scroll

## About Scroll

Scroll is a Wayland compositor forked from Sway that implements a scrolling layout similar to PaperWM. While maintaining compatibility with most Sway/i3 configurations, it offers additional features:

- Animations with customizable N-order Bezier curves
- Independent content scaling for windows
- Overview and Jump modes for efficient window management
- Workspace scaling
- Trackpad/Mouse scrolling for workspace navigation
- Support for both portrait and landscape monitor layouts

## Configuration profiles

The Scroll package in Fedora defers most of the dependencies and the config file ownership to the `scroll-config-*` subpackages. This allows us to ship different configuration profiles with different sets of runtime dependencies. This also allows anyone to create a package with their preferred system-wide configuration defaults and use it instead of the default Fedora profiles.

The profiles currently defined in the `scroll` source package are the following:

- **scroll-config-upstream** - the upstream configuration. The only permitted modifications to the config file are adjustments for dependencies currently unavailable in Fedora.
- **scroll-config-minimal** - minimal configuration with any optional dependencies omitted. Suitable for headless servers, containers and buildroot usage.

The config packages are mutually exclusive, and one of these must always be installed. The one selected by default is **scroll-config-upstream**. At any moment, you can switch the installed configuration with one of the following commands:

```
dnf swap scroll-config scroll-config-upstream
dnf swap scroll-config scroll-config-minimal
# for a third-party configuration profile:
dnf swap scroll-config scroll-config-custom
```

The command will replace the default `/etc/scroll/config` file and apply the new set of dependencies. Packages unused by the new profile will be autoremoved.

## Scroll-specific features

Unlike standard Sway, Scroll uses a scrolling layout by default. You can find detailed documentation about Scroll's unique features in the included manual pages:

```
man 5 scroll
man 1 scroll
man 1 scrollmsg
man 7 scroll-ipc
```

## Custom profile example

An example spec header for a custom configuration profile:

```
Name:           scroll-config-custom
Version:        1.0
Release:        1%{?dist}
Summary:        Custom configuration for Scroll
BuildArch:      noarch
Requires:       scroll >= 0.1.0
Provides:       scroll-config = %{version}-%{release}
Conflicts:      scroll-config

# common dependencies
# ...

# profile dependencies
Requires:       waybar

%files
%config(noreplace) %{_sysconfdir}/scroll/config
# Session file also belongs to the configuration subpackage;
# Otherwise we won't be able to add a wrapper script or set additional properties
%{_datadir}/wayland-sessions/scroll.desktop
```
