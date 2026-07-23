#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "server" / "mercatus_launch_studio.py"


def load_server():
    spec = importlib.util.spec_from_file_location("mercatus_launch_studio", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_templates() -> None:
    data = json.loads((ROOT / "data" / "launch_templates.json").read_text(encoding="utf-8"))
    assert len(data.get("templates", [])) >= 3
    assert len(data.get("onboarding_steps", [])) >= 6


def test_launch_package() -> None:
    module = load_server()
    state = module.LaunchState()
    status, package = state.create_package(json.loads((ROOT / "examples" / "launch-package.json").read_text(encoding="utf-8")))
    assert status == 201
    assert package["package_hash"]
    assert package["pricing"]["recommended_price"] > 0
    assert "Go Live" in package["onboarding_steps"]


if __name__ == "__main__":
    test_templates()
    test_launch_package()
    print("mercatus smoke tests passed")
