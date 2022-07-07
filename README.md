# grafana-pcp
The grafana-pcp package

## Setup instructions
* clone the upstream sources: `git clone https://github.com/performancecopilot/grafana-pcp && cd grafana-pcp`
* checkout the version of the specfile: `git checkout <currentversion>`
* apply existing patches: `git am ../0*.patch`

## Upgrade instructions
* follow the Setup instructions above
* rebase to the new version: `git fetch && git rebase --onto <newversion> <oldversion>`
  * rebasing `remove-unused-frontend-crypto.patch`: only apply the patch to `package.json` and run `yarn install`, then `yarn.lock` will get updated automatically
* create new patches from the modified git commits: `git format-patch -N --no-stat --no-signature <newversion> && mv *.patch ..`
* update `Version`, `Release`, `%changelog` and tarball NVRs in the specfile
* create bundles and manifest: `./create_bundles_in_container.sh`
* update specfile with contents of the `.manifest` file
* run local build: `rpkg local`
* run rpmlint: `rpmlint -r grafana-pcp.rpmlintrc /tmp/rpkg/grafana-pcp-*/grafana-pcp-*.src.rpm /tmp/rpkg/grafana-pcp-*/x86_64/grafana-pcp-*.x86_64.rpm`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources *.tar.gz *.tar.xz`
* commit new `sources` file

## Patches
* create the patch
* declare and apply (`%prep`) the patch in the specfile
* if the patch affects Go or Node.js dependencies, or the webpack
  * add the patch to `PATCHES_PRE_VENDOR` or `PATCHES_PRE_WEBPACK` in the Makefile
  * create new tarballs
  * update the specfile with new tarball name and contents of the `.manifest` file

### General guidelines
* aim to apply all patches in the specfile
* avoid rebuilding the tarballs

Patches fall in several categories:
  * modify dependency versions
  * modify both sources and vendored dependencies (e.g. CVEs)
  * modify the Node.js source (i.e. affect the webpack)
  * some patches are conditional (e.g. FIPS)

Patches cannot be applied twice.
It is not possible to unconditionally apply all patches in the Makefile, and great care must be taken to include the required patches at the correct stage of the build.

## Reproducible Bundles
Run `./create_bundles_in_container.sh` to generate a reproducible vendor and webpack bundle.
