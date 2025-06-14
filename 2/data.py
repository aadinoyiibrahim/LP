# data.py
import pandas as pd
from typing import Tuple, Dict, List


def load_data(
    warehouses_csv: str = './data/warehouses.csv',
    customers_csv: str  = './data/customers.csv',
    distances_csv: str  = './data/distances.csv'
) -> Tuple[List[str], List[str], Dict[str, float], Dict[str, int], Dict[str, int], Dict[Tuple[str, str], float]]:
    """
    Loads CSV files from the ./data directory by default and returns:
      - list of warehouse IDs
      - list of customer IDs
      - fixed cost dict
      - capacity dict
      - demand dict
      - cost dict (warehouse_id, customer_id) -> cost
    """
    wh = pd.read_csv(warehouses_csv)
    cust = pd.read_csv(customers_csv)
    dist = pd.read_csv(distances_csv)

    W = wh['id'].tolist()
    C = cust['id'].tolist()

    fixed_cost = dict(zip(wh['id'], wh['fixed_cost']))
    capacity   = dict(zip(wh['id'], wh['capacity']))
    demand     = dict(zip(cust['id'], cust['demand']))
    cost = {
        (row['warehouse_id'], row['customer_id']): row['cost']
        for _, row in dist.iterrows()
    }

    return W, C, fixed_cost, capacity, demand, cost