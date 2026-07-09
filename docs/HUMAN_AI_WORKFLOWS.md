# Human and AI Workflows

## Human Operator Flow

1. Validate launch templates: `python tools/mercatusctl.py validate`.
2. Pick a launch template with `python tools/mercatusctl.py templates`.
3. Estimate pricing with `python tools/mercatusctl.py price`.
4. Run the API server: `python server/mercatus_launch_studio.py --port 8780`.
5. Submit `examples/launch-package.json` to `POST /launch-packages`.
6. Review the generated price, proof gates, onboarding steps, and go-live checklist.
7. Export the package into README, website, PDF, or sales material only after claim review.

## AI Worker Flow

1. Read `mercatus-launch-studio.manifest.json`.
2. Read `data/launch_templates.json`.
3. Generate a launch package from product metadata.
4. Return price assumptions and proof gates.
5. Do not publish claims without a compliance note and go-live checklist.

## Proof Outputs

- Launch package hash
- Pricing inputs
- Onboarding steps
- Go-live checklist
- Claim-check proof gates

## Live Test Commands

```bash
python tools/mercatusctl.py validate
python tests/smoke_test.py
python benchmarks/benchmark_launch_packages.py
python server/mercatus_launch_studio.py --port 8780
```
