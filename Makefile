all: grafana-pcp-$(VER).tar.gz \
	 grafana-pcp-vendor-$(VER).tar.xz \
	 grafana-pcp-webpack-$(VER).tar.gz

grafana-pcp-$(VER).tar.gz:
	wget https://github.com/performancecopilot/grafana-pcp/archive/v$(VER)/grafana-pcp-$(VER).tar.gz

ALL_PATCHES := $(wildcard *.patch)
PATCHES_TO_APPLY := $(ALL_PATCHES)

grafana-pcp-vendor-$(VER).tar.xz: grafana-pcp-$(VER).tar.gz
	rm -rf grafana-pcp-$(VER)
	tar xfz grafana-pcp-$(VER).tar.gz

	# patches can affect Go or Node.js dependencies, or the webpack
	for patch in $(PATCHES_TO_APPLY); do patch -d grafana-pcp-$(VER) -p1 --fuzz=0 < $$patch; done

	# Go
	cd grafana-pcp-$(VER) && go mod vendor -v
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' grafana-pcp-$(VER)/go.mod | \
		sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@.manifest

	# Node.js
	cd grafana-pcp-$(VER) && yarn install --pure-lockfile
	# Remove files with licensing issues
	find grafana-pcp-$(VER) -type d -name 'node-notifier' -prune -exec rm -r {} \;
	find grafana-pcp-$(VER) -type f -name '*.exe' -delete
	# Remove not required packages
	rm -r grafana-pcp-$(VER)/node_modules/puppeteer
	./list_bundled_nodejs_packages.py grafana-pcp-$(VER)/ >> $@.manifest

	# Jsonnet
	cd grafana-pcp-$(VER) && jb --jsonnetpkg-home=vendor_jsonnet install

	# Create tarball
	XZ_OPT=-9 tar cfJ $@ \
		grafana-pcp-$(VER)/vendor \
		grafana-pcp-$(VER)/node_modules \
		grafana-pcp-$(VER)/vendor_jsonnet

grafana-pcp-webpack-$(VER).tar.gz: grafana-pcp-$(VER).tar.gz
	cd grafana-pcp-$(VER) && \
		../build_frontend.sh

	tar cfz $@ grafana-pcp-$(VER)/dist

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm grafana-pcp-*/
