all: grafana-pcp-$(VER).tar.gz \
	 grafana-pcp-vendor-$(VER).tar.xz \
	 grafana-pcp-webpack-$(VER).tar.gz

grafana-pcp-$(VER).tar.gz grafana-pcp-$(VER)/:
	wget https://github.com/performancecopilot/grafana-pcp/archive/v$(VER)/grafana-pcp-$(VER).tar.gz
	rm -rf grafana-pcp-$(VER)
	tar xfz grafana-pcp-$(VER).tar.gz
	cd grafana-pcp-$(VER) && shopt -s nullglob && \
		for patch in ../*.patch; do patch -p1 < $$patch; done

grafana-pcp-vendor-$(VER).tar.xz: grafana-pcp-$(VER)/
	# Go
	cd grafana-pcp-$(VER) && go mod vendor -v
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' grafana-pcp-$(VER)/go.mod | \
		sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@.manifest

	# Node.js
	cd grafana-pcp-$(VER) && yarn install --pure-lockfile
	# Remove files with licensing issues
	find grafana-pcp-$(VER) -type d -name 'node-notifier' -prune -exec rm -r {} \;
	find grafana-pcp-$(VER) -name '*.exe' -delete
	# Remove not required packages
	rm -r grafana-pcp-$(VER)/node_modules/puppeteer
	./list_bundled_nodejs_packages.py grafana-pcp-$(VER)/ >> $@.manifest

	# Jsonnet
	cd grafana-pcp-$(VER) && jb --jsonnetpkg-home=vendor_jsonnet install

	# Create tarball
	XZ_OPT=-9 tar cfJ $@ \
		grafana-pcp-$(VER)/vendor \
		$$(find grafana-pcp-$(VER) -type d -name "node_modules" -prune) \
		grafana-pcp-$(VER)/vendor_jsonnet

grafana-pcp-webpack-$(VER).tar.gz: grafana-pcp-$(VER)/
	cd grafana-pcp-$(VER) && \
		yarn install --pure-lockfile && \
		make dist-dashboards dist-frontend && \
		chmod -R g-w,o-w dist

	tar cfz $@ grafana-pcp-$(VER)/dist

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm grafana-pcp-*/
