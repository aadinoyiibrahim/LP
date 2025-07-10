#!/usr/bin/env python3
import argparse
from calc import add, subtract, multiply

def main():
    parser = argparse.ArgumentParser(
        description="Simple CLI Calculator"
    )
    parser = argparse.ArgumentParser(description="Simple Python Calculator")
    parser.add_argument(
        "operation",
        choices=["add", "subtract", "multiply"],
        help="Operation to perform"
    )
    parser.add_argument("x", type=float, help="First number")
    parser.add_argument("y", type=float, help="Second number")
    args = parser.parse_args()

    if args.operation == "add":
        result = add(args.x, args.y)
    elif args.operation == "subtract":
        result = subtract(args.x, args.y)
    else:
        result = multiply(args.x, args.y)
    parser.add_argument("x", help="First number")
    parser.add_argument("y", help="Second number")
    args = parser.parse_args()

    # Validate and convert inputs
    try:
        x = float(args.x)
        y = float(args.y)
    except ValueError:
        parser.error("Both x and y must be valid numbers")

    # Dispatch to the correct function
    if args.operation == "add":
        result = add(x, y)
    elif args.operation == "subtract":
        result = subtract(x, y)
    else:
        result = multiply(x, y)

    print(f"Result: {args.operation} {args.x} & {args.y} gives {result}")

if __name__ == "__main__":
    main()
