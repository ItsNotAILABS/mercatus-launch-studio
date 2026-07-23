#!/usr/bin/env python3
"""mercatusctl: local CLI for Mercatus Launch Studio."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_PATH = ROOT / "data" / "launch_templates.json"


def load_templates() -> dict[str, Any]:
    return json.loads(TEMPLATES_PATH.read_text(encoding="utf-8"))


def validate() -> int:
    data = load_templates()
    templates = data.get("templates", [])
    errors: list[str] = []
    if not templates:
        errors.append("templates must be non-empty")
    for index, template in enumerate(templates):
        for field in ("id", "name", "sections", "default_audience"):
            if field not in template:
                errors.append(f"templates[{index}] missing {field}")
    if errors:
        print("mercatusctl validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"mercatusctl validation passed: {len(templates)} templates")
    return 0


def list_templates() -> int:
    for template in load_templates().get("templates", []):
        print(f"{template['id']}\t{template['name']}")
    return 0


def price(args: argparse.Namespace) -> int:
    value = args.base_value * args.complexity_multiplier * args.proof_multiplier + args.support_premium
    print(json.dumps({
        "recommended_price": round(value, 2),
        "formula": "base_value * complexity_multiplier * proof_multiplier + support_premium",
        "review_required": True,
    }, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Mercatus launch studio CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("templates")
    price_parser = sub.add_parser("price")
    price_parser.add_argument("--base-value", type=float, default=5000)
    price_parser.add_argument("--complexity-multiplier", type=float, default=1.25)
    price_parser.add_argument("--proof-multiplier", type=float, default=1.1)
    price_parser.add_argument("--support-premium", type=float, default=750)
    args = parser.parse_args()
    if args.command == "validate":
        return validate()
    if args.command == "templates":
        return list_templates()
    if args.command == "price":
        return price(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
