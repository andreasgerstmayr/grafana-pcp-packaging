# grafana-pcp

The grafana-pcp package

## Build instructions
```
VER=1.0.4
spectool -g grafana-pcp.spec
./create_dependency_bundle.sh $(pwd)/grafana-pcp-$VER.tar.gz $(pwd)/grafana-pcp-deps-$VER.tar.xz
./check_npm_dependencies.py grafana-pcp.spec grafana-pcp-$VER.tar.gz grafana-pcp-deps-$VER.tar.xz
fedpkg new-sources grafana-pcp-$VER.tar.gz grafana-pcp-deps-$VER.tar.xz

fedpkg local
fedpkg lint
fedpkg mockbuild
fedpkg scratch-build --srpm

fedpkg build
fedpkg update
```
