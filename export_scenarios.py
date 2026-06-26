"""CLI wrapper for generating scenarios.json from the simulation engine."""

from __future__ import annotations

import argparse
import json

from simulation import run_simulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate World Cup scenario probabilities")
    parser.add_argument(
        "--simulations",
        type=int,
        default=5000,
        help="Number of Monte Carlo runs (default: 5000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional RNG seed for reproducible output",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="scenarios.json",
        help="Output JSON file path (default: scenarios.json)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = run_simulation(simulations=args.simulations, seed=args.seed)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)
    print(f"Exported to {args.output}")


if __name__ == "__main__":
    main()
