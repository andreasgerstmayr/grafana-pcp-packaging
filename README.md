# grafana-pcp
The grafana-pcp package

## Upgrade instructions
(replace X.Y.Z with the new grafana-pcp version)

* update `Version`, `Release` and `%changelog` in the specfile
* create bundles and manifest: `VER=X.Y.Z make clean all`
* update specfile with contents of the `.manifest` file
* run local build: `rpkg local`
* run rpm linter: `rpkg lint -r grafana-pcp.rpmlintrc`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources *.tar.gz`

## Backporting
* create the patch
* declare and apply (`%prep`) the patch in the specfile
* if the patch affects Go or Node.js dependencies, or the webpack
  * create new tarballs and rename them to `grafana-pcp-...-X.Y.Z-R.tar.gz`
  * update the specfile with new tarball path and contents of the `.manifest` file

Note: the Makefile automatically applies all patches before creating the tarballs
