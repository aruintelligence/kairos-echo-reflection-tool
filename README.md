# Kairos Echo

A reproducible Python coherence simulator and browser reflection tool with an auditable, scripted veto rule.

[![Release](https://img.shields.io/github/v/release/aruintelligence/kairos-echo-reflection-tool?style=flat-square)](https://github.com/aruintelligence/kairos-echo-reflection-tool/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.8+-2563eb?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-16a34a?style=flat-square)](LICENSE)
[![Repository stars](https://img.shields.io/github/stars/aruintelligence/kairos-echo-reflection-tool?style=flat-square)](https://github.com/aruintelligence/kairos-echo-reflection-tool/stargazers)

> **Scope:** Kairos Echo is a poetic, contemplative research tool—not therapy, meditation instruction, spiritual authority, or a measurement of consciousness.

## What it includes

- Deterministic simulations with seeded random-number generation
- Coherence, distortion, and stability dynamics
- A Guardian Veto™ rule that blocks outward actions when simulated coherence is low, with a configurable coherence penalty
- A paired, three-arm audit: configured veto penalty, zero-penalty veto, and no veto, using identical sampled actions and deltas
- Trekchö- and Tögal-inspired reflection prompts
- CLI modes for runs, summaries, logging, and reflection
- A standalone browser interface in `kairos-echo.html`
- Optional Plotly visualization when Plotly is installed

## Quick start

```bash
git clone https://github.com/aruintelligence/kairos-echo-reflection-tool.git
cd kairos-echo-reflection-tool
python -m pip install numpy
python kairos_echo.py --mode run --steps 500 --seed 42
python kairos_echo.py --mode summary
python kairos_echo.py --mode togal
python kairos_echo.py --mode audit --steps 300 --seed 42 --replicates 32 --audit-file audit.json
```

For dashboard mode:

```bash
python -m pip install plotly
python kairos_echo.py --mode dashboard --save-html dashboard.html
```

You can also open `kairos-echo.html` directly in a modern browser.

## Reproducibility

Use a fixed `--seed` to reproduce a trajectory. The audit uses seeds `seed` through `seed + replicates - 1`; for each seed, the proposed actions and sampled deltas match exactly under all three policies. It reports per-seed mean and final coherence, veto counts, and differences in mean coherence relative to no veto. The JSON has no timestamp, so identical parameters produce identical audit files.

The default veto subtracts 0.18 from coherence when it blocks an outward action. That can lower this simulator's coherence compared with letting the sampled outward delta through. The zero-penalty arm holds coherence constant on a veto, isolating the penalty's effect from blocking. Run the audit before interpreting the veto as beneficial, and vary the model parameters to inspect sensitivity. Neither coherence nor the veto is a measure of actual ethical behavior or safety. The browser page is an unseeded, simplified visual companion; its trajectories are not paired with the Python audit.

For the command above (300 steps, seeds 42–73), mean coherence was **0.0588 lower** under the configured penalty than without veto (29 of 32 seeds lower). With the veto penalty set to zero, mean coherence was **0.0055 higher** than without veto (24 of 32 seeds higher). These outcomes describe the default toy dynamics only; the zero-penalty arm does not change the normal run mode.

Treat all values as simulator state—not clinical, psychological, or spiritual measurements.

## Related projects

- [Kairos Echo Inward Mirror](https://github.com/aruintelligence/kairos-echo-inward-mirror)
- [Kairos Coherence Simulator](https://github.com/aruintelligence/kairos-coherence-simulator)
- [ĀRU Intelligence public research](https://github.com/aruintelligence/aru-intelligence-ai)

## License

Released under the [MIT License](LICENSE). Dzogchen terms belong to living religious traditions and are used here respectfully as inspiration, without claiming lineage or authority.
