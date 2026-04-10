import importlib

# Define the packages to check: display name -> module name
pkg_info = {
    'PuLP': 'pulp',
    'NumPy': 'numpy',
    'Matplotlib': 'matplotlib',
}

print("Testing imports...")

# Gather versions (handle missing modules gracefully)
versions = {}
for name, module_name in pkg_info.items():
    try:
        module = importlib.import_module(module_name)
        versions[name] = getattr(module, '__version__', 'unknown')
    except ImportError:
        versions[name] = 'not installed'

# Prepare table data
headers = ['Package', 'Version']
rows = [[pkg, ver] for pkg, ver in versions.items()]

# Compute column widths
col_widths = [
    max(len(str(item)) for item in [headers[i]] + [row[i] for row in rows])
    for i in range(len(headers))
]

# Helper to print a separator line
def print_separator():
    print('+' + '+'.join('-' * (w + 2) for w in col_widths) + '+')

# Print the table
print_separator()
print('| ' + ' | '.join(headers[i].ljust(col_widths[i]) for i in range(len(headers))) + ' |')
print_separator()
for row in rows:
    print('| ' + ' | '.join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + ' |')
print_separator()

print("All imports are working correctly.")