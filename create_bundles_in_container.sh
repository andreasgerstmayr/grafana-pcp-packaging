#!/bin/bash -eu
#
# create vendor and webpack bundles inside a container for reproducibility
# using a Go cache:
#   ./create_bundles_in_container.sh -v $(pwd)/.gocache:/root/go:z
#

cat <<EOF | podman build -t grafana-pcp-build -f - .
FROM fedora:35

RUN dnf upgrade -y && \
    dnf install -y rpmdevtools python3-packaging make golang nodejs yarnpkg golang-github-jsonnet-bundler golang-github-google-jsonnet

WORKDIR /tmp/grafana-pcp-build
COPY Makefile grafana-pcp.spec *.patch build_frontend.sh list_bundled_nodejs_packages.py .
RUN mkdir bundles
CMD make && mv *.tar.* bundles
EOF

podman run --name grafana-pcp-build --replace "$@" grafana-pcp-build
podman cp grafana-pcp-build:bundles/. .
