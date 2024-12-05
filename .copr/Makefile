.PHONY: prepare goprep rustprep pythonprep themesprep srpm prebuild

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
