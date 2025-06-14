# facility.py
from pyomo.environ import (
    ConcreteModel, Set, Param, Var,
    NonNegativeReals, Binary, Constraint,
    Objective, minimize, SolverFactory
)
from typing import List, Dict, Tuple
from data import load_data


class FacilityLocationModel:
    """
    Encapsulates the capacitated facility-location MIP using Pyomo.
    """
    def __init__(
        self,
        warehouses_csv: str = './data/warehouses.csv',
        customers_csv: str  = './data/customers.csv',
        distances_csv: str  = './data/distances.csv'
    ):
        # Load data
        (
            self.W,
            self.C,
            self.fixed_cost,
            self.capacity,
            self.demand,
            self.cost
        ) = load_data()
        self._build_model()

    def _build_model(self):
        m = ConcreteModel()
        m.W = Set(initialize=self.W)
        m.C = Set(initialize=self.C)
        m.fixed = Param(m.W, initialize=self.fixed_cost)
        m.cap   = Param(m.W, initialize=self.capacity)
        m.dem   = Param(m.C, initialize=self.demand)
        m.cost  = Param(m.W, m.C, initialize=self.cost, default=1e6)

        # Variables
        m.y = Var(m.W, domain=Binary)
        m.x = Var(m.W, m.C, domain=NonNegativeReals)


        # Constraints
        def demand_rule(mdl, j):
            return sum(mdl.x[i,j] for i in mdl.W) >= mdl.dem[j]
        m.Demand = Constraint(m.C, rule=demand_rule)

        def cap_rule(mdl, i):
            return sum(mdl.x[i,j] for j in mdl.C) <= mdl.cap[i] * mdl.y[i]
        m.Capacity = Constraint(m.W, rule=cap_rule)

        # Objective
        def obj_rule(mdl):
            return (
                sum(mdl.fixed[i]*mdl.y[i] for i in mdl.W) +
                sum(mdl.cost[i,j]*mdl.x[i,j] for i in mdl.W for j in mdl.C)
            )
        m.Obj = Objective(rule=obj_rule, sense=minimize)

        self.model = m

    def solve(self, solver_name: str, time_limit: int = 60, mip_gap: float = 0.01):
        """
        Solve the model with given solver, time limit (sec), and mip_gap.
        Returns the solver results object.
        """
        solver = SolverFactory(solver_name)
        if solver_name.lower() == 'glpk':
            solver.options['tmlim']  = time_limit
            solver.options['mipgap'] = mip_gap
        else:
            solver.options['sec']   = time_limit
            solver.options['ratio'] = mip_gap

        logfile = f"{solver_name}.log"
        results = solver.solve(self.model, tee=False,  logfile=logfile)
        return results, logfile

    def get_solution(self) -> Dict[str, Dict[str, float]]:
        """
        Extracts the open facilities and shipment plan.
        """
        sol = {'opened': [], 'shipments': {}}
        for i in self.W:
            if self.model.y[i].value > 0.5:
                sol['opened'].append(i)
                sol['shipments'][i] = {
                    j: self.model.x[i,j].value
                    for j in self.C if self.model.x[i,j].value > 1e-6
                }
        return sol


if __name__ == '__main__':
    fl = FacilityLocationModel('warehouses.csv', 'customers.csv', 'distances.csv')
    res = fl.solve('cbc')
    print(f"Objective: {fl.model.Obj():.2f}")
    print(fl.get_solution())