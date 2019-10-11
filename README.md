# grafana-pcp

The grafana-pcp package

## Build
```
spectool -g -R grafana-pcp.spec
./create_dependency_bundle.sh VER ~/rpmbuild/SOURCES/grafana-pcp-deps-VER.tar.xz
./check_npm_dependencies.py grafana-pcp.spec ~/rpmbuild/SOURCES/grafana-pcp-VER.tar.gz ~/rpmbuild/SOURCES/grafana-pcp-deps-VER.tar.xz
```
