#!/usr/bin/env python3
import argparse
from calc import add, subtract, multiply


def main():
    parser = argparse.ArgumentParser(
        description="Simple CLI Calculator"
    )
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

    print(f"Result: {args.operation} {args.x} & {args.y} gives {result}")


if __name__ == "__main__":
    main()
