#!/usr/bin/env python3
import argparse

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

    print(f"{args.operation.title()} {args.x} and {args.y}")

if __name__ == "__main__":
    main()
