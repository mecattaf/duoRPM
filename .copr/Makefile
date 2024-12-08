.PHONY: prepare goprep rustprep pythonprep themesprep srpm prebuild

specfile = $(notdir $(spec))

prepare:
	dnf install --nodocs -y rpm-build rpmdevtools

# Go package preparation with vendoring support
goprep:
	dnf install --nodocs -y \
		--repofrompath 'golang-rawhide,https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/fedora-$$releasever-$$basearch/' \
		--setopt='golang-rawhide.gpgkey=https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/pubkey.gpg' \
		golang git-core
	go env -w GOPROXY=https://proxy.golang.org,direct
	go env -w GOSUMDB=sum.golang.org
	if [ -f bundle_go_deps_for_rpm.sh ]; then \
		bash bundle_go_deps_for_rpm.sh $(specfile); \
	fi

# Rust package preparation
rustprep:
	dnf install --nodocs -y \
		rust cargo git-core pkg-config

# Python package preparation
pythonprep:
	dnf install --nodocs -y \
		python3-devel python3-pip python3-wheel python3-setuptools

# Theme and static content preparation with Python support
themesprep:
	dnf install --nodocs -y \
		git-core python3-devel python3-pip python3-wheel

# Determine build type and apply appropriate preparation
prebuild:
	@if grep -q "Name:.*wl-gammarelay-rs" $(specfile); then \
		$(MAKE) rustprep; \
	elif grep -q "Name:.*cliphist\|Name:.*nwg-look" $(specfile); then \
		$(MAKE) goprep; \
	elif grep -q "Name:.*python-autotiling\|Name:.*nwg-clipman" $(specfile); then \
		$(MAKE) pythonprep; \
	elif grep -q "Name:.*bibata-cursor-themes" $(specfile); then \
		$(MAKE) themesprep; \
	else \
		echo "Unknown package type. Check spec file: $(specfile)"; \
		exit 1; \
	fi

srpm: prepare prebuild
	spectool -g ./$(specfile)
	rpmbuild -bs \
		--define "_sourcedir ${PWD}" \
		--define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" \
		--define "_srcrpmdir $(outdir)" \
		--define "_rpmdir ${PWD}" \
		--define "_buildrootdir ${PWD}/.build" \
		$(specfile)
