# metrics.py
import time
import pandas as pd
import resource
import re
from pyomo.opt import SolverFactory
from facility import FacilityLocationModel

def benchmark_solvers(
    solvers: list,
    warehouses_csv: str = './data/warehouses.csv',
    customers_csv: str = './data/customers.csv',
    distances_csv: str = './data/distances.csv',
    time_limit: int = 60,
    mip_gap: float = 0.01
) -> pd.DataFrame:
    """
    Runs each solver on the same model and records:
      - solve time
      - objective
      - status
      - optimality gap (if exposed)
      - node count (parsed from solver log)
      - peak memory (MB)
    """
    records = []
    for s in solvers:
        solver = SolverFactory(s)
        if not solver.available(exception_flag=False):
            records.append({
                'solver': s,
                'time_s': None,
                'objective': None,
                'status': 'unavailable',
                'gap': None,
                'nodes': None,
                'memory_mb': None
            })
            continue

        # Build & solve
        fl = FacilityLocationModel(warehouses_csv, customers_csv, distances_csv)
        t0 = time.time()
        try:
            # facility.solve now returns (results, logfile)
            res, logfile = fl.solve(s, time_limit, mip_gap)

            # time & memory
            time_s = time.time() - t0
            peak_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
            memory_mb = peak_kb / 1024.0

            # read the solver's text log
            with open(logfile, 'r') as f:
                log = f.read()

            # parse node count
            if s.lower() == 'cbc':
                m = re.search(r'Total .*?(\d+)\s+\d+\.\d+%', log)
                nodes = int(m.group(1)) if m else None
            elif s.lower() == 'glpk':
                m = re.search(r'(\d+)\s+nodes', log)
                nodes = int(m.group(1)) if m else None
            elif s.lower() == 'scip':
                m = re.search(r'nodes\s*:\s*([0-9]+)', log)
                nodes = int(m.group(1)) if m else None
            else:
                nodes = None

            # gap (if provided by Pyomo)
            gap = getattr(res.solver, 'gap', None)

            records.append({
                'solver': s,
                'time_s': time_s,
                'objective': float(fl.model.Obj()),
                'status': res.solver.termination_condition,
                'gap': gap,
                'nodes': nodes,
                'memory_mb': memory_mb
            })

        except Exception as e:
            records.append({
                'solver': s,
                'time_s': None,
                'objective': None,
                'status': f'error: {e}',
                'gap': None,
                'nodes': None,
                'memory_mb': None
            })

    return pd.DataFrame(records)


if __name__ == '__main__':
    df = benchmark_solvers(['glpk', 'cbc', 'scip'])
    print(df)
