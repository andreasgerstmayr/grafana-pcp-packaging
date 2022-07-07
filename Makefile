VERSION := $(shell rpm --specfile *.spec --qf '%{VERSION}\n' | head -1)
RELEASE := $(shell rpm --specfile *.spec --qf '%{RELEASE}\n' | head -1 | cut -d. -f1)
CHANGELOGTIME := $(shell rpm --specfile *.spec --qf '%{CHANGELOGTIME}\n' | head -1)
SOURCE_DATE_EPOCH := $(shell echo $$(( $(CHANGELOGTIME) - $(CHANGELOGTIME) % 86400 )))

NAME       := grafana-pcp
RPM_NAME   := $(NAME)
SOURCE_DIR := $(NAME)-$(VERSION)
SOURCE_TAR := $(NAME)-$(VERSION).tar.gz
VENDOR_TAR := $(RPM_NAME)-vendor-$(VERSION)-$(RELEASE).tar.xz
WEBPACK_TAR := $(RPM_NAME)-webpack-$(VERSION)-$(RELEASE).tar.gz

# patches which must be applied before creating the vendor tarball, for example:
# - changes in dependency versions
# - changes in Go module imports (which affect the vendored Go modules)
PATCHES_PRE_VENDOR := \
	0001-remove-unused-frontend-crypto.patch \

# patches which must be applied before creating the webpack, for example:
# - changes in Node.js sources or vendored dependencies
PATCHES_PRE_WEBPACK := \
	0001-remove-unused-frontend-crypto.patch \
	0002-Revert-all-rename-plugin-IDs-from-pcp-to-performance.patch \


all: $(SOURCE_TAR) $(VENDOR_TAR) $(WEBPACK_TAR)

$(SOURCE_TAR):
	spectool -g $(RPM_NAME).spec

$(VENDOR_TAR): $(SOURCE_TAR)
	# Start with a clean state
	rm -rf $(SOURCE_DIR)
	tar pxf $(SOURCE_TAR)

	# Patches to apply before vendoring
	for patch in $(PATCHES_PRE_VENDOR); do echo applying $$patch ...; patch -d $(SOURCE_DIR) -p1 --fuzz=0 < $$patch; done

	# Go
	cd $(SOURCE_DIR) && go mod vendor -v
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' $(SOURCE_DIR)/go.mod | \
		sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@.manifest

	# Node.js
	cd $(SOURCE_DIR) && yarn install --frozen-lockfile
	# Remove files with licensing issues
	find $(SOURCE_DIR) -type d -name 'node-notifier' -prune -exec rm -r {} \;
	find $(SOURCE_DIR) -type f -name '*.exe' -delete
	./list_bundled_nodejs_packages.py $(SOURCE_DIR) >> $@.manifest

	# Jsonnet
	cd $(SOURCE_DIR) && jb --jsonnetpkg-home=vendor_jsonnet install

	# Create tarball
	XZ_OPT=-9 tar \
		--sort=name \
		--mtime="@$(SOURCE_DATE_EPOCH)" --clamp-mtime \
		--owner=0 --group=0 --numeric-owner \
		-cJf $@ \
		$(SOURCE_DIR)/vendor \
		$(SOURCE_DIR)/node_modules \
		$(SOURCE_DIR)/vendor_jsonnet

$(WEBPACK_TAR): $(VENDOR_TAR)
	# Start with a clean state
	rm -rf $(SOURCE_DIR)
	tar pxf $(SOURCE_TAR)
	tar pxf $(VENDOR_TAR)

	# Patches to apply before creating the webpack
	for patch in $(PATCHES_PRE_WEBPACK); do echo applying $$patch ...; patch -d $(SOURCE_DIR) -p1 --fuzz=0 < $$patch; done

	# Build frontend
	cd $(SOURCE_DIR) && \
		../build_frontend.sh

	# Create tarball
	tar \
		--sort=name \
		--mtime="@$(SOURCE_DATE_EPOCH)" --clamp-mtime \
		--owner=0 --group=0 --numeric-owner \
		-czf $@ \
		$(SOURCE_DIR)/dist

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm $(NAME)-*/
