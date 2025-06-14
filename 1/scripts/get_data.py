#!/usr/bin/env python3
"""
Fetch a small LP test-suite into ../data/.

• Netlib LP collection  – via Coin-OR GitHub (main branch) or a SourceForge mirror
• Two real-world models – railway.mps and power.mps
• One synthetic dense LP (2 000 × 2 000)

Run from the project root:
    python scripts/get_data.py
"""

import io, sys, tarfile, zipfile
from pathlib import Path

import requests
from scipy import sparse
import pulp

# ------------------------------------------------------------------ #
# 0. Destination folder                                               #
# ------------------------------------------------------------------ #
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
print(f"✔ Data directory is {DATA_DIR}")

# ------------------------------------------------------------------ #
# 1. Netlib LP collection                                             #
# ------------------------------------------------------------------ #
def fetch_netlib() -> None:
    """Download Netlib .mps files (≈12 MB uncompressed)."""
    sources = [
        # Coin-OR repo (main branch tarball)
        "https://github.com/coin-or/linear-programming-data/"
        "archive/refs/heads/main.tar.gz",
        # SourceForge mirror
        "https://downloads.sourceforge.net/project/lpnetlib/netlib_lp_data.zip",
    ]

    print("\n=== Netlib LP collection ===")
    for url in sources:
        host = url.split("/", 3)[2]
        try:
            print(f"  ↳ trying {host} …")
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            buf = io.BytesIO(resp.content)

            if url.endswith(".zip"):
                with zipfile.ZipFile(buf) as zf:
                    names = [n for n in zf.namelist() if n.endswith(".mps")]
                    for n in names:
                        (DATA_DIR / Path(n).name).write_bytes(zf.read(n))
            else:  # .tar.gz
                with tarfile.open(fileobj=buf, mode="r:gz") as tar:
                    members = [m for m in tar.getmembers() if m.name.endswith(".mps")]
                    for m in members:
                        m.name = Path(m.name).name        # strip folders
                        tar.extract(m, DATA_DIR)
            print(f"  ✓ extracted {len(list(DATA_DIR.glob('*.mps')))} .mps files")
            return                                      # SUCCESS → stop loop
        except Exception as e:
            print(f"    ⚠ {e}")

    sys.exit("✖ All Netlib sources failed – check your network connection.")

# ------------------------------------------------------------------ #
# 2. Real-world models                                                #
# ------------------------------------------------------------------ #
def fetch_single_models() -> None:
    print("\n=== Real-world LPs ===")
    urls = {
        "railway.mps": "https://zenodo.org/record/8389589/files/railway.mps?download=1",
        "power.mps":   "https://gitlab.com/openmod-optim/uc-texas/-/raw/main/data/power.mps",
    }
    for fname, url in urls.items():
        dest = DATA_DIR / fname
        if dest.exists():
            print(f"  ✓ {fname} already present")
            continue
        print(f"  ↳ downloading {fname} …")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"    saved ({dest.stat().st_size/1e6:.1f} MB)")

# ------------------------------------------------------------------ #
# 3. Synthetic dense LP                                               #
# ------------------------------------------------------------------ #
def generate_dense() -> None:
    fname = DATA_DIR / "denseRnd_2000.lp"
    if fname.exists():
        print("\n=== Synthetic dense LP already present ===")
        return
    print("\n=== Generating synthetic dense LP ===")
    A = sparse.random(2000, 2000, density=0.4, format="csr", random_state=42)
    pb = pulp.LpProblem("denseRnd", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(2000)]
    pb += pulp.lpSum((j + 1) * v for j, v in enumerate(x))
    for i in range(2000):
        pb += pulp.lpDot(A.getrow(i).toarray().ravel(), x) <= 1000
    pb.writeLP(fname)
    print(f"  ✓ written {fname.relative_to(PROJECT_ROOT)} "
          f"({fname.stat().st_size/1e6:.1f} MB)")

# ------------------------------------------------------------------ #
# 4. Main                                                             #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    fetch_netlib()
    fetch_single_models()
    generate_dense()
    print("\nAll done!  Sample of data/:")
    for f in sorted(DATA_DIR.glob('*'))[:10]:
        print(" •", f.name)
    if len(list(DATA_DIR.iterdir())) > 10:
        print("   …")
