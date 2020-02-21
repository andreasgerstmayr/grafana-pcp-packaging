#!/bin/bash -eu

SRC=$(readlink -f "${1:?Usage: $0 source destination}")
DEST=$(readlink -f "${2:?Usage: $0 source destination}")

if [ -f "$DEST" ]; then
    echo "File $DEST exists already."
    exit 0
fi
if [ "$#" -gt 2 ]; then
    PATCHES=$(readlink -f "${@:3}")
else
    PATCHES=""
fi

pushd "$(mktemp -d)"

echo Extracting sources...
tar xfz "$SRC"
cd grafana-pcp-*

echo Applying patches...
for patch in $PATCHES
do
    patch -p1 < $patch
done

echo Installing dependencies...
yarn install

echo Removing files with licensing issues...
rm -rf node_modules/node-notifier

echo Compressing...
XZ_OPT=-9 tar cJf "$DEST" node_modules

popd
