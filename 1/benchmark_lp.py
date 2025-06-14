#!/usr/bin/env python3
"""Benchmark open-source LP solvers on a curated instance list."""

import argparse, csv, re, subprocess, time, psutil, sys, numpy as np
from pathlib import Path
import re

# ──────────────────────────────────────────────────────────────
# 0)  CURATED BENCHMARK LIST  – edit here if you want changes
# ──────────────────────────────────────────────────────────────
KEEP = {
    "afiro.mps", "sc50a.mps", "blend.mps", "share2b.mps",
    "woodw.mps", "adlittle.mps", "ship08s.mps",
    "pilot.mps", "pds-20.mps",
    "railway.mps", "power.mps", "denseRnd_2000.lp",
}

# ──────────────────────────────────────────────────────────────
# 1)  Solver command templates
# ──────────────────────────────────────────────────────────────
SOLVERS = {
    "highs": ["highs", "--presolve", "on", "--solver", "simplex"],
    "glpk":  ["glpsol", "--lp"],          # works for .mps too
    "clp":   ["clp"],
}

# ──────────────────────────────────────────────────────────────
# 2)  Regex helpers for log parsing
# ──────────────────────────────────────────────────────────────
_status = re.compile(
    r"(?:Status *: *(\w+))|"          # HiGHS
    r"(?:OPTIMAL LP SOLUTION FOUND)|" # GLPK
    r"(?:Optimal - objective)",       # CLP
    re.I
)
_iters = re.compile(
    r"(?:Iterations|Simplex Iterations|Total iterations"
    r"|Iterations performed\s*:\s*([0-9]+))",  # CLP barrier
    re.I
)


def _parse(stdout: str):
    # status
    if      "OPTIMAL LP SOLUTION FOUND" in stdout.upper(): status = "Optimal"
    elif    "OPTIMAL - OBJECTIVE"       in stdout.upper(): status = "Optimal"
    elif    "Status" in stdout: status = _status.search(stdout).group(1)
    else:   status = "Unknown"

    # iterations
    m_iters = _iters.search(stdout)
    # iters   = float(m_iters.group(1)) if m_iters else np.nan
    iters = (next((float(g) for g in m_iters.groups() if g), np.nan)
    if m_iters else np.nan)
    
    # gap
    m_gap = re.search(r"Gap *: *([0-9.eE+-]+)", stdout)
    gap   = float(m_gap.group(1)) if m_gap else 0.0
    return status, iters, gap

def _run_once(model: Path, solver: str):
    cmd  = SOLVERS[solver] + [str(model)]
    t0   = time.perf_counter()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    child = psutil.Process(proc.pid)
    rss_peak = 0
    while proc.poll() is None:
        rss_peak = max(rss_peak, child.memory_info().rss)
        time.sleep(0.05)
    stdout = proc.stdout.read()
    secs   = time.perf_counter() - t0
    status, iters, gap = _parse(stdout)
    return [model.name, solver, secs, rss_peak/1e6, iters, gap, status]

# ──────────────────────────────────────────────────────────────
# 4)  CLI
# ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-folder", type=Path, default="data",
                    help="Folder containing .lp / .mps files")
    ap.add_argument("--repeat", type=int, default=3,
                    help="Cold runs per instance/solver")
    ap.add_argument("--out", default="results.csv",
                    help="Destination CSV file")
    ap.add_argument("--keep-file", type=Path,
                    help="Optional text file (one filename per line) overriding the hard-coded KEEP list")
    args = ap.parse_args()

    # choose the whitelist
    if args.keep_file and args.keep_file.exists():
        keep = {l.strip() for l in args.keep_file.read_text().splitlines() if l.strip()}
    else:
        keep = KEEP

    # gather models
    models = [p for p in args.data_folder.iterdir()
              if p.name in keep and p.suffix in {".lp", ".mps"}]

    if not models:
        sys.exit(f"No matching models found in {args.data_folder}. Check KEEP list or paths.")

    # benchmark
    with open(args.out, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["instance", "solver", "secs",
                         "rss_mb", "iterations", "gap", "status"])
        for m in models:
            for solver in SOLVERS:
                for _ in range(args.repeat):
                    writer.writerow(_run_once(m, solver))
                    fh.flush()

if __name__ == "__main__":
    main()
