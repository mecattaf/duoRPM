I am working on setting up a Fedora COPR repository that will be managed through GitHub Actions. The repository will contain both my own custom packages and some packages from solopasha's hyprlandRPM repository. I have already:
1. Set up the COPR repository (zenRPM)
2. Created the GitHub Actions workflows
3. Configured GitHub repository secrets with COPR authentication
4. Created the basic repository structure
I need help with adapting individual .spec files and creating corresponding update.sh scripts to work with this automated system. I will provide:
- The current .copr/Makefile
- The GitHub Actions workflows (update.yml and build.yml)
- The .spec file we need to work on
- Examples of working update.sh scripts
The system uses commit message triggers for builds:
- [build-all] builds everything
- [build-go] builds Go packages
- [build-rust] builds Rust packages
- [build-python] builds Python packages
- [build-themes] builds theme packages
Each package needs:
1. A properly formatted .spec file compatible with COPR building
2. An update.sh script that:
   - Checks for new versions from the appropriate source
   - Updates the spec file correctly
   - Uses the right build trigger in commit messages
   - Handles version string formatting appropriately
Here are my current workflow files:
[I will paste my current .copr/Makefile here]

```
.PHONY: prepare goprep rustprep pythonprep srpm

specfile = $(notdir $(spec))

prepare:
	dnf install --nodocs -y rpm-build rpmdevtools

# Go package preparation
goprep:
	dnf install --nodocs -y --repofrompath 'golang-rawhide,https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/fedora-$$releasever-$$basearch/' \
		--setopt='golang-rawhide.gpgkey=https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/pubkey.gpg' golang git-core
	go env -w GOPROXY=https://proxy.golang.org,direct
	go env -w GOSUMDB=sum.golang.org
	bash bundle_go_deps_for_rpm.sh $(specfile)

# Rust package preparation
rustprep:
	dnf install --nodocs -y rust cargo git-core
	# We'll vendor dependencies during prep phase in spec file

# Python package preparation
pythonprep:
	dnf install --nodocs -y python3-devel python3-pip python3-wheel

# Theme and static content preparation
themesprep:
	dnf install --nodocs -y git-core

# Determine build type and apply appropriate preparation
prebuild:
	@if grep -q "BuildRequires:.*cargo" $(specfile); then \
		$(MAKE) rustprep; \
	elif grep -q "BuildRequires:.*golang" $(specfile) || grep -q "%gometa" $(specfile); then \
		$(MAKE) goprep; \
	elif grep -q "BuildRequires:.*python" $(specfile); then \
		$(MAKE) pythonprep; \
	else \
		$(MAKE) themesprep; \
	fi

srpm: prepare prebuild
	spectool -g ./$(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" $(specfile)

```

[I will paste my current .github/workflows/update.yml here]

```
name: Update package versions

on:
  workflow_dispatch:
  schedule:
    - cron: '45 */6 * * *'  # Run every 6 hours, offset by 45 minutes

jobs:
  main:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    container:
      image: 'registry.fedoraproject.org/fedora-minimal:latest'

    steps:
      - name: Prepare
        run: |
          microdnf -y install --nodocs --setopt=install_weak_deps=0 \
            git-core rpm-build curl perl-interpreter jq rpmdevtools copr-cli parallel \
            python3-pip golang cargo  # Added for version checking of various package types

      - name: Copr config
        env:
          COPR_CONF: ${{ secrets.COPR_CONFIG }}
        run: |
          mkdir -p ~/.config
          echo "$COPR_CONF" > ~/.config/copr

      - uses: actions/checkout@v4

      - name: Run updater
        run: |
          git config --global --add safe.directory "$GITHUB_WORKSPACE"
          git config --local user.name "github-actions[bot]"
          git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
          find -name "update.sh" -execdir {} \;

```

[I will paste my current .github/workflows/build.yml here]

```
name: Build packages

on:
  workflow_dispatch:
  push:
    paths:
      - '**/*.spec'
      - '.copr/**'
      - '.github/**'

jobs:
  main:
    if: |
      github.event_name == 'workflow_dispatch' ||
      contains(github.event.head_commit.message, '[build-all]') ||
      contains(github.event.head_commit.message, '[build-go]') ||
      contains(github.event.head_commit.message, '[build-rust]') ||
      contains(github.event.head_commit.message, '[build-python]') ||
      contains(github.event.head_commit.message, '[build-themes]')
    runs-on: ubuntu-latest
    container:
      image: 'registry.fedoraproject.org/fedora-minimal:latest'

    steps:
      - name: Prepare
        run: |
          microdnf -y install --nodocs --setopt=install_weak_deps=0 \
            copr-cli parallel

      - name: Copr config
        env:
          COPR_CONF: ${{ secrets.COPR_CONFIG }}
        run: |
          mkdir -p ~/.config
          echo "$COPR_CONF" > ~/.config/copr

      - uses: actions/checkout@v4

      # Build Go packages (cliphist and nwg-look)
      - name: Build Go packages
        if: github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[build-all]') || contains(github.event.head_commit.message, '[build-go]')
        run: |
          # Build cliphist first as it's a dependency
          cliphist_build_id=$(copr-cli build-package mecattaf/zenRPM --nowait --name cliphist | sed -n 's/.*builds: \(.*\)/\1'/p)
          # Build nwg-look after cliphist
          copr-cli build-package mecattaf/zenRPM --nowait --name nwg-look --after-build-id "$cliphist_build_id"

      # Build Rust package
      - name: Build Rust package
        if: github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[build-all]') || contains(github.event.head_commit.message, '[build-rust]')
        run: |
          copr-cli build-package mecattaf/zenRPM --nowait --name wl-gammarelay-rs

      # Build Python packages
      - name: Build Python packages
        if: github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[build-all]') || contains(github.event.head_commit.message, '[build-python]')
        run: |
          # Build nwg-clipman after cliphist
          copr-cli build-package mecattaf/zenRPM --nowait --name nwg-clipman --after-build-id "$cliphist_build_id"
          copr-cli build-package mecattaf/zenRPM --nowait --name python-autotiling

      # Build theme packages
      - name: Build theme packages
        if: github.event_name == 'workflow_dispatch' || contains(github.event.head_commit.message, '[build-all]') || contains(github.event.head_commit.message, '[build-themes]')
        run: |
          parallel copr-cli build-package mecattaf/zenRPM --nowait --name ::: \
            bibata-cursor-themes \
            catppuccin-theme

      # Optional status check for all builds
      - name: Check build status
        if: always()
        run: |
          sleep 30  # Give COPR time to register all builds
          copr-cli list-builds mecattaf/zenRPM --with-details

```

For this specific package, here is the current .spec file:
[I will paste the .spec file we need to work on]
We are currently working on: ``

My current spec file:
```
```


Please help me:
1. Review and modify the .spec file if needed to work with our automated system
2. Create an appropriate update.sh script for this package
[a proposed update.sh file found below FOR INSPIRATION - NOTE IT HAS TO DO WITH ANOTHER SPEC FILE]
```
# cliphist/update.sh
#!/bin/bash
set -euo pipefail

SPEC="cliphist.spec"
REPO="sentriz/cliphist"

LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
    git add "$SPEC"
    git commit -m "Update cliphist to $LATEST [build-go]"
    git push
fi

# wl-gammarelay-rs/update.sh
#!/bin/bash
set -euo pipefail

SPEC="wl-gammarelay-rs.spec"
REPO="MaxVerevkin/wl-gammarelay-rs"

LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
    git add "$SPEC"
    git commit -m "Update wl-gammarelay-rs to $LATEST [build-rust]"
    git push
fi

# python-autotiling/update.sh
#!/bin/bash
set -euo pipefail

SPEC="python-autotiling.spec"
PYPI_NAME="autotiling"

LATEST=$(curl -s "https://pypi.org/pypi/${PYPI_NAME}/json" | jq -r .info.version)
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    sed -i "s/%global pypi_version.*/%global pypi_version ${LATEST}/" "$SPEC"
    git add "$SPEC"
    git commit -m "Update python-autotiling to $LATEST [build-python]"
    git push
fi

# bibata-cursor-themes/update.sh
#!/bin/bash
set -euo pipefail

SPEC="bibata-cursor-themes.spec"
REPO="ful1e5/Bibata_Cursor"

LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
    git add "$SPEC"
    git commit -m "Update bibata-cursor-themes to $LATEST [build-themes]"
    git push
fi
```
3. Explain any changes needed to integrate this package into our build system
Note: The packages need to be built in the correct order due to dependencies:
- cliphist must be built first as others depend on it
- nwg-clipman depends on cliphist
- Other packages can be built in parallel
Some packages come from solopasha's repository:
- cliphist (Go package)
- nwg-clipman (Python package)
- nwg-look (Go package)
And some are my custom packages:
- wl-gammarelay-rs (Rust package)
- bibata-cursor-themes (Theme package)
- catppuccin-theme (Theme package)
- python-autotiling (Python package)
