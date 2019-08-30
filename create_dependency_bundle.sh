#!/bin/bash
set -e

VER="${1:?Usage: $0 version destination}"
DEST="${2:?Usage: $0 version destination}"

if [ -f "$DEST" ]; then
    echo "File $DEST exists already."
    exit 0
fi

pushd $(mktemp -d)
wget https://github.com/performancecopilot/grafana-pcp/archive/v$VER/grafana-pcp-$VER.tar.gz
tar xfz grafana-pcp-$VER.tar.gz
cd grafana-pcp-$VER
yarn install
echo "Compressing..."
XZ_OPT=-9 tar cJf $DEST node_modules
popd
