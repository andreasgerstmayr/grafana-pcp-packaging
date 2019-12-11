#!/bin/bash
set -e

SRC="${1:?Usage: $0 source destination}"
DEST="${2:?Usage: $0 source destination}"

if [ -f "$DEST" ]; then
    echo "File $DEST exists already."
    exit 0
fi

pushd $(mktemp -d)
tar xfz $SRC
cd grafana-pcp-*
yarn install
echo "Compressing..."
XZ_OPT=-9 tar cJf $DEST node_modules
popd
