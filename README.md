# Kairos Echo

A reproducible Python coherence simulator and browser reflection tool with an explicit ethical guardrail.

[![Release](https://img.shields.io/github/v/release/aruintelligence/kairos-echo-reflection-tool?style=flat-square)](https://github.com/aruintelligence/kairos-echo-reflection-tool/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.8+-2563eb?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-16a34a?style=flat-square)](LICENSE)
[![Repository stars](https://img.shields.io/github/stars/aruintelligence/kairos-echo-reflection-tool?style=flat-square)](https://github.com/aruintelligence/kairos-echo-reflection-tool/stargazers)

> **Scope:** Kairos Echo is a poetic, contemplative research tool—not therapy, meditation instruction, spiritual authority, or a measurement of consciousness.

## What it includes

- Deterministic simulations with seeded random-number generation
- Coherence, distortion, and stability dynamics
- A Guardian Veto™ that limits outward action when simulated coherence is low
- Trekchö- and Tögal-inspired reflection prompts
- CLI modes for runs, summaries, logging, and reflection
- A standalone browser interface in `kairos-echo.html`
- Optional Plotly visualization when Plotly is installed

## Quick start

```bash
git clone https://github.com/aruintelligence/kairos-echo-reflection-tool.git
cd kairos-echo-reflection-tool
python kairos_echo.py --mode run --steps 500 --seed 42
python kairos_echo.py --mode summary
python kairos_echo.py --mode togal
```

For dashboard mode:

```bash
python -m pip install plotly
python kairos_echo.py --mode dashboard --save-html dashboard.html
```

You can also open `kairos-echo.html` directly in a modern browser.

## Reproducibility

Use a fixed `--seed` to reproduce a trajectory. Treat the values as simulator state—not clinical, psychological, or spiritual measurements.

## Related projects

- [Kairos Echo Inward Mirror](https://github.com/aruintelligence/kairos-echo-inward-mirror)
- [Kairos Coherence Simulator](https://github.com/aruintelligence/kairos-coherence-simulator)
- [ĀRU Intelligence public research](https://github.com/aruintelligence/aru-intelligence-ai)

## License

Released under the [MIT License](LICENSE). Dzogchen terms belong to living religious traditions and are used here respectfully as inspiration, without claiming lineage or authority.
