# Mercatus Launch Studio

![Status](https://img.shields.io/badge/status-platform%20buildout-blue)
![Launch](https://img.shields.io/badge/launch%20templates-3-6f42c1)
![Python](https://img.shields.io/badge/python-stdlib%20server-3776ab)
![Pricing](https://img.shields.io/badge/pricing-advisor-2f9e44)
![Onboarding](https://img.shields.io/badge/onboarding-6%20steps-0b7285)

Launch studio for product pages, pricing advisors, onboarding flows, creator profiles, and customer-safe outreach guardrails.

Mercatus turns a product manifest into a launch package: positioning, onboarding, pricing, proof gates, and go-live checklist.

## Quick Start

Validate templates:

```bash
python tools/mercatusctl.py validate
```

List launch templates and price a package:

```bash
python tools/mercatusctl.py templates
python tools/mercatusctl.py price --base-value 7500 --complexity-multiplier 1.35 --proof-multiplier 1.2 --support-premium 1200
```

Run the API:

```bash
python server/mercatus_launch_studio.py --port 8780
```

Call the API:

```bash
curl http://127.0.0.1:8780/health
curl http://127.0.0.1:8780/templates
curl -s -X POST http://127.0.0.1:8780/launch-packages -H 'content-type: application/json' -d @examples/launch-package.json
```

## Platform Surfaces

| Surface | Path |
| --- | --- |
| Platform manifest | `mercatus-launch-studio.manifest.json` |
| Launch templates | `data/launch_templates.json` |
| API server | `server/mercatus_launch_studio.py` |
| CLI | `tools/mercatusctl.py` |
| Example package request | `examples/launch-package.json` |

## Pricing Formula

```text
recommended_price = base_value * complexity_multiplier * proof_multiplier + support_premium
```

The formula is advisory, not automatic billing. Every price recommendation requires human review.

## Six-Step Launch Onboarding

1. Brand
2. Content
3. Features
4. Updates
5. Go Live
6. Customer Success

## Operating Law

- Do not publish unsupported claims.
- Every launch package must include proof gates.
- Pricing advice must include inputs and assumptions.
- Outreach must stay customer-safe and compliance-aware.
- Go-live requires README/product page, pricing review, onboarding path, and support loop.

## Search Keywords

AI launch studio, product launch automation, pricing advisor, app marketplace launch, creator profile builder, onboarding flow generator, go-live checklist, NOVA Build launch tools, business automation launch package.

## Next Gates

- Persist launch packages.
- Add Markdown/PDF export.
- Connect to SpecForge project specs.
- Add dashboard UI.
