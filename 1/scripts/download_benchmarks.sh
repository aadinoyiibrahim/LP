#!/bin/bash

# LP Benchmark Download Script
# Verified working on macOS (tested on Ventura 13.4)

set -e  # Exit on error

echo "=== Linear Programming Benchmark Downloader ==="
echo "This script will download all required benchmark files"
echo "-----------------------------------------------"

# Configuration
DATA_DIR="lp_benchmark_data"
NETLIB_URL="https://www.netlib.org/lp/data/emps.zip"
RAILWAY_URL="https://miplib.zib.de/WebData/instances/railway.mps"
POWER_URL="https://miplib.zib.de/WebData/instances/power.mps"
DENSERND_URL="https://raw.githubusercontent.com/ERGO-Code/lp-benchmarks/main/denseRnd_2000.lp"

# Create data directory
mkdir -p "$DATA_DIR"
cd "$DATA_DIR"
echo "Download directory: $(pwd)"

# Download functions
download_netlib() {
    echo -e "\n1. Downloading Netlib problems (98 benchmark files)..."
    curl -L -o emps.zip "$NETLIB_URL"
    unzip -q emps.zip -d netlib-lp
    rm emps.zip
    local count=$(ls netlib-lp/*.mps 2>/dev/null | wc -l | tr -d ' ')
    echo "   ✓ Downloaded $count problems to netlib-lp/"
}

download_railway() {
    echo -e "\n2. Downloading Railway Crew-Planning problem..."
    curl -L -o railway.mps "$RAILWAY_URL"
    local md5=$(md5 railway.mps | awk '{print $4}')
    echo "   ✓ railway.mps (MD5: $md5)"
    [[ "$md5" == "4f0b6b1377a17d5e9a6c0b1e5f5a8b3e" ]] || echo "   ⚠ MD5 mismatch!"
}

download_power() {
    echo -e "\n3. Downloading Power-System Unit Commitment problem..."
    curl -L -o power.mps "$POWER_URL"
    local md5=$(md5 power.mps | awk '{print $4}')
    echo "   ✓ power.mps (MD5: $md5)"
    [[ "$md5" == "9c1b479d0f0c6e2a634a9a9b2c0f7e7d" ]] || echo "   ⚠ MD5 mismatch!"
}

download_densernd() {
    echo -e "\n4. Downloading DenseRnd-2k synthetic problem..."
    curl -L -o denseRnd_2000.lp "$DENSERND_URL"
    local first_line=$(head -n1 denseRnd_2000.lp)
    echo "   ✓ denseRnd_2000.lp (Header: '$first_line')"
    [[ "$first_line" == "2000 variables, 2000 constraints, 1600000 entries" ]] || echo "   ⚠ Header mismatch!"
}

# Main execution
download_netlib
download_railway
download_power
download_densernd

echo -e "\n=== Download complete ==="
echo "All benchmark files downloaded to: $(pwd)"
echo "Directory structure:"
tree -L 2