# plot.py
import os
import matplotlib.pyplot as plt
import pandas as pd
from metrics import benchmark_solvers

# Ensure the output directory exists
os.makedirs('plot', exist_ok=True)

def load_results():
    return benchmark_solvers(
        ['glpk', 'cbc', 'scip'],
        './data/warehouses.csv',
        './data/customers.csv',
        './data/distances.csv'
    )

def show_table(df: pd.DataFrame, column: str, fmt: str = '{:.4g}'):
    """
    Prints a neat solver vs. metric table.
    """
    table = df[['solver', column]].copy()
    table[column] = table[column].map(lambda x: fmt.format(x) if isinstance(x, (int, float)) else x)
    print(f"\n=== {column.replace('_',' ').title()} by Solver ===")
    print(table.to_string(index=False))

def plot_metric(df: pd.DataFrame, column: str, ylabel: str, kind: str = 'bar'):
    """
    Creates, saves, and displays a single chart for the given metric.
    """
    fig, ax = plt.subplots()
    df.plot(x='solver', y=column, kind=kind, legend=False, ax=ax)
    ax.set_xlabel('Solver')
    ax.set_ylabel(ylabel)
    # ax.set_title(f'{ylabel} Comparison')
    plt.tight_layout()

    # Save the figure
    filename = f"plot/{column}.png"
    fig.savefig(filename)
    print(f"Saved plot to {filename}")

    plt.show()

def main():
    df = load_results()

    metrics = [
        ('time_s',     'Solve Time (s)',         '{:.2f}'),
        ('objective',  'Objective Value',        '{:.2f}'),
        ('gap',        'Optimality Gap (%)',     '{:.2f}'),
        ('nodes',      'Branch-and-Bound Nodes', '{}')
    ]

    for col, label, fmt in metrics:
        show_table(df, col, fmt)
        plot_metric(df, col, label)

if __name__ == '__main__':
    main()
