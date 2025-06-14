#!/usr/bin/env bash
# Pull 98 Netlib models + 2 industrial LPs into ./data
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="$ROOT/data";  mkdir -p "$DATA"

echo "───────────────────────────────────────────────────────────────"
echo " 1) Netlib  (98   × .mps from GitHub mirror)"
echo "───────────────────────────────────────────────────────────────"
TMP=$(mktemp -d)
git clone --depth 1 https://github.com/zrjer/LP-TEST-PROBLEM-FROM-NETLIB.git "$TMP" >/dev/null
cp "$TMP/netlib_mps/"*.mps "$DATA/"
count_netlib=$(ls "$DATA"/*.mps | wc -l)
rm -rf "$TMP"
echo "    ✓ copied $count_netlib Netlib files"

echo "───────────────────────────────────────────────────────────────"
echo " 2) Railway crew-planning model"
echo "───────────────────────────────────────────────────────────────"
curl -Lf -o "$DATA/railway.mps" \
     "https://zenodo.org/doi/10.5281/zenodo.8389589"
echo "    ✓ railway.mps saved"

echo "───────────────────────────────────────────────────────────────"
echo " 3) Power-system unit-commitment model"
echo "───────────────────────────────────────────────────────────────"
TMP2=$(mktemp -d)
git clone --depth 1 https://gitlab.com/openmod-optim/uc-texas.git "$TMP2" >/dev/null
cp "$TMP2/data/power.mps" "$DATA/"
rm -rf "$TMP2"
echo "    ✓ power.mps saved"

echo "───────────────────────────────────────────────────────────────"
echo " ✔  Done — $(ls "$DATA" | wc -l) files now in data/"
echo "───────────────────────────────────────────────────────────────"
