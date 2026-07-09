#!/usr/bin/env python3
"""Mercatus Launch Studio development server."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_PATH = ROOT / "data" / "launch_templates.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_templates() -> dict[str, Any]:
    return json.loads(TEMPLATES_PATH.read_text(encoding="utf-8"))


def stable_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def pricing_advice(payload: dict[str, Any]) -> dict[str, Any]:
    base_value = float(payload.get("base_value", 5000))
    complexity = float(payload.get("complexity_multiplier", 1.25))
    proof = float(payload.get("proof_multiplier", 1.1))
    support = float(payload.get("support_premium", 750))
    price = round(base_value * complexity * proof + support, 2)
    return {
        "recommended_price": price,
        "formula": "base_value * complexity_multiplier * proof_multiplier + support_premium",
        "inputs": {
            "base_value": base_value,
            "complexity_multiplier": complexity,
            "proof_multiplier": proof,
            "support_premium": support,
        },
        "review_required": true,
    }


class LaunchState:
    def __init__(self) -> None:
        self.templates = load_templates()
        self.template_map = {item["id"]: item for item in self.templates.get("templates", [])}

    def health(self) -> dict[str, Any]:
        return {"status": "ok", "service": "mercatus-launch-studio", "time": utc_now(), "template_count": len(self.template_map)}

    def create_package(self, request: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        template_id = request.get("template_id", "developer-platform")
        template = self.template_map.get(template_id)
        if not template:
            return 404, {"status": "rejected", "reason": "unknown_template", "known_templates": sorted(self.template_map)}
        product = request.get("product", {}) if isinstance(request.get("product", {}), dict) else {}
        pricing = pricing_advice(request.get("pricing", {}) if isinstance(request.get("pricing", {}), dict) else {})
        package = {
            "schema": "nova.mercatus.launch_package.v1",
            "status": "draft",
            "template_id": template_id,
            "product": {
                "name": product.get("name", "Untitled NOVA Product"),
                "audience": product.get("audience", template.get("default_audience")),
                "one_line_offer": product.get("one_line_offer", "A launch-ready NOVA product surface."),
            },
            "sections": template.get("sections", []),
            "onboarding_steps": self.templates.get("onboarding_steps", []),
            "pricing": pricing,
            "go_live_checklist": [
                "README and product page complete",
                "claim check complete",
                "pricing assumptions reviewed",
                "onboarding path verified",
                "support contact and feedback loop assigned",
            ],
            "proof_gates": ["claim check", "price formula inputs", "audience fit", "compliance note", "go-live checklist"],
            "created_at": utc_now(),
        }
        package["package_hash"] = stable_hash(package)
        return 201, package


class Handler(BaseHTTPRequestHandler):
    state: LaunchState

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        print(f"[{utc_now()}] {self.address_string()} {format % args}")

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self.send_json(200, self.state.health())
        elif path == "/templates":
            self.send_json(200, self.state.templates)
        else:
            self.send_json(404, {"paths": ["/health", "/templates", "POST /launch-packages", "POST /pricing"]})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            body = self.read_json_body()
        except json.JSONDecodeError as exc:
            self.send_json(400, {"status": "rejected", "reason": "invalid_json", "detail": str(exc)})
            return
        if path == "/launch-packages":
            status, payload = self.state.create_package(body)
            self.send_json(status, payload)
        elif path == "/pricing":
            self.send_json(200, pricing_advice(body))
        else:
            self.send_json(404, {"paths": ["POST /launch-packages", "POST /pricing"]})


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Mercatus Launch Studio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8780)
    args = parser.parse_args()
    Handler.state = LaunchState()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Mercatus Launch Studio listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
