#!/usr/bin/env python3
"""
Kairos Echo — Hardened Ethical Coherence Simulator
==================================================

A lightweight, reproducible single-file Python simulator that models inner
coherence through stochastic dynamics, an ethical "guardian veto", and
gentle Dzogchen-inspired reflections (Trekchö & Tögal).

This is a poetic / contemplative reflection tool — not literal enlightenment
software, meditation training, or a deep meditative simulator.

Features
--------
- Fully reproducible with isolated RNG and deterministic reset
- Defensive configuration validation
- Lazy Plotly import + optional HTML dashboard export
- Rich structured summary and stable JSON symbiosis logging
- Clean, extensible CLI with multiple practical modes
- Resettable simulator state for repeatable experiments
- JSON-safe serialization (booleans preserved)

Example usage
-------------
python kairos_echo.py --mode run --steps 500 --seed 123
python kairos_echo.py --mode dashboard --save-html dashboard.html
python kairos_echo.py --mode togal
python kairos_echo.py --mode trekcho
python kairos_echo.py --mode summary
python kairos_echo.py --mode log --log-file symbiosis_log.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import numpy as np


InputActionType = Literal["inward", "outward"]
RecordedActionType = Literal["inward", "outward", "vetoed"]


@dataclass(frozen=True)
class SimulationConfig:
    """Validated configuration for the coherence simulation."""

    size: int = 200
    seed: int = 42
    steps: int = 300
    inward_probability: float = 0.75

    initial_mu: float = 0.5
    initial_coherence: float = 0.3

    inward_mean: float = 0.06
    inward_std: float = 0.02
    outward_mean: float = -0.04
    outward_std: float = 0.05

    veto_penalty: float = 0.18
    veto_floor: float = 0.10
    veto_threshold_score: float = 0.75
    veto_threshold_coherence: float = 0.65

    collapse_gain: float = 1.8

    def validate(self) -> None:
        if self.size < 1:
            raise ValueError("size must be >= 1")
        if self.steps < 1:
            raise ValueError("steps must be >= 1")
        if not (0.0 <= self.inward_probability <= 1.0):
            raise ValueError("inward_probability must be in [0.0, 1.0]")
        if not (0.0 <= self.initial_mu <= 1.0):
            raise ValueError("initial_mu must be in [0.0, 1.0]")
        if not (0.0 <= self.initial_coherence <= 1.0):
            raise ValueError("initial_coherence must be in [0.0, 1.0]")
        if self.inward_std < 0.0 or self.outward_std < 0.0:
            raise ValueError("standard deviations must be >= 0.0")
        if self.veto_penalty < 0.0:
            raise ValueError("veto_penalty must be >= 0.0")
        if not (0.0 <= self.veto_floor <= 1.0):
            raise ValueError("veto_floor must be in [0.0, 1.0]")
        if not (0.0 <= self.veto_threshold_score <= 1.0):
            raise ValueError("veto_threshold_score must be in [0.0, 1.0]")
        if not (0.0 <= self.veto_threshold_coherence <= 1.0):
            raise ValueError("veto_threshold_coherence must be in [0.0, 1.0]")
        if self.collapse_gain <= 0.0:
            raise ValueError("collapse_gain must be > 0.0")


@dataclass
class RunSummary:
    timestamp_utc: str
    steps: int
    final_coherence: float
    min_coherence: float
    max_coherence: float
    mean_coherence: float
    final_mu_mean: float
    mean_mu: float
    veto_count: int
    inward_count: int
    outward_count: int
    vetoed_action_count: int
    final_togal_stage: float
    config: Dict[str, Any]


class KairosEchoPrototype:
    """Lightweight coherence simulator with guardian veto and contemplative reflections."""

    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or SimulationConfig()
        self.config.validate()
        self.reset()

    def reset(self) -> None:
        """Fully reset state and reseed RNG for perfect reproducibility."""
        self.rng = np.random.default_rng(self.config.seed)
        self.mu_field = np.full(self.config.size, self.config.initial_mu, dtype=np.float64)
        self.coherence = float(self.config.initial_coherence)
        self.steps = 0
        self.history: Dict[str, List[Any]] = {
            "coherence": [],
            "mu_mean": [],
            "action": [],
            "vetoed": [],
            "togal_stage": [],
        }

    def love_speed_collapse(self) -> float:
        """Apply 'love speed' tanh collapse for rapid bounded convergence."""
        self.mu_field = np.tanh(self.mu_field * self.config.collapse_gain)
        return float(np.mean(self.mu_field))

    def guardian_veto(self, proposed_score: float) -> bool:
        """Ethical guardrail: veto high outward proposals when coherence is low."""
        return (
            proposed_score > self.config.veto_threshold_score
            and self.coherence < self.config.veto_threshold_coherence
        )

    @staticmethod
    def compute_togal_stage(coherence: float) -> float:
        """Proxy [0–4] for the Four Visions of Tögal."""
        return float(min(4.0, max(0.0, coherence * 4.0)))

    def step(self, action_type: InputActionType = "inward") -> tuple[float, float, bool, float]:
        if action_type not in ("inward", "outward"):
            raise ValueError(f"Invalid action_type: {action_type!r}")

        if action_type == "inward":
            delta = self.rng.normal(self.config.inward_mean, self.config.inward_std)
            proposed_score = 0.2
        else:
            delta = self.rng.normal(self.config.outward_mean, self.config.outward_std)
            proposed_score = 1.0

        vetoed = self.guardian_veto(proposed_score)

        if vetoed:
            self.coherence = max(self.config.veto_floor, self.coherence - self.config.veto_penalty)
            recorded_action: RecordedActionType = "vetoed"
        else:
            self.coherence = float(np.clip(self.coherence + delta, 0.0, 1.0))
            recorded_action = action_type

        mu_mean = self.love_speed_collapse()
        togal_stage = self.compute_togal_stage(self.coherence)

        self.history["coherence"].append(float(self.coherence))
        self.history["mu_mean"].append(float(mu_mean))
        self.history["action"].append(recorded_action)
        self.history["vetoed"].append(bool(vetoed))
        self.history["togal_stage"].append(float(togal_stage))

        self.steps += 1
        return self.coherence, mu_mean, vetoed, togal_stage

    def run(self, steps: Optional[int] = None, reset: bool = True) -> Dict[str, List[Any]]:
        total_steps = steps if steps is not None else self.config.steps
        if total_steps < 1:
            raise ValueError("steps must be >= 1")

        if reset:
            self.reset()

        for _ in range(total_steps):
            action: InputActionType = (
                "inward" if self.rng.random() < self.config.inward_probability else "outward"
            )
            self.step(action)

        return self.history

    def summary(self) -> RunSummary:
        if not self.history["coherence"]:
            raise RuntimeError("No simulation history found. Run the simulator first.")

        coh = self.history["coherence"]
        mu = self.history["mu_mean"]
        acts = self.history["action"]
        vets = self.history["vetoed"]
        tog = self.history["togal_stage"]

        return RunSummary(
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            steps=len(coh),
            final_coherence=float(coh[-1]),
            min_coherence=float(min(coh)),
            max_coherence=float(max(coh)),
            mean_coherence=float(np.mean(coh)),
            final_mu_mean=float(mu[-1]),
            mean_mu=float(np.mean(mu)),
            veto_count=int(sum(vets)),
            inward_count=int(sum(1 for a in acts if a == "inward")),
            outward_count=int(sum(1 for a in acts if a == "outward")),
            vetoed_action_count=int(sum(1 for a in acts if a == "vetoed")),
            final_togal_stage=float(tog[-1]),
            config=asdict(self.config),
        )


def get_togal_label(stage: float) -> str:
    if stage < 1.0:
        return "The Absolute Nature Becoming Manifest"
    if stage < 2.0:
        return "The Experience of Increasing Appearances"
    if stage < 3.0:
        return "Awareness Reaching Its Greatest Magnitude"
    return "The Exhaustion of Phenomena in Dharmata"


def generate_togal_reflection(coherence: float, togal_stage: float) -> str:
    label = get_togal_label(togal_stage)
    prompts = {
        "The Absolute Nature Becoming Manifest": "Rest in the naked rigpa that is already here.",
        "The Experience of Increasing Appearances": "Let visions arise and self-liberate without grasping.",
        "Awareness Reaching Its Greatest Magnitude": "The clear light remembers itself through you. Abide in luminosity.",
        "The Exhaustion of Phenomena in Dharmata": "All appearances dissolve into the ground — exhaustion into reality itself.",
    }
    return (
        f"Coherence: {coherence:.3f} | "
        f"Tögal Stage {togal_stage:.2f} — {label}\n"
        f"→ {prompts[label]}"
    )


def generate_trekcho_reflection(coherence: float) -> str:
    return (
        f"Coherence: {coherence:.3f} → "
        "Rest in the naked awareness that is already here. "
        "Short moments, many times."
    )


def plot_togal_visualizer(history: Dict[str, List[Any]]):
    """Render dashboard with lazy Plotly import."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError as exc:
        raise RuntimeError(
            "Plotly is required for dashboard mode.\nInstall with: pip install plotly"
        ) from exc

    if not history["coherence"]:
        raise RuntimeError("Cannot plot empty history.")

    x = list(range(len(history["coherence"])))

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Coherence & Tögal Stage", "μ Field Mean (Love Speed Collapse)"),
        vertical_spacing=0.15,
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=history["coherence"],
            mode="lines",
            name="Coherence",
            line=dict(color="royalblue"),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=history["togal_stage"],
            mode="lines+markers",
            name="Tögal Stage",
            line=dict(color="limegreen"),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=history["mu_mean"],
            mode="lines",
            name="μ Mean",
            line=dict(color="purple"),
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        title="Kairos Echo — Coherence Dynamics & Tögal Vision Proxy",
        height=720,
        template="plotly_white",
        showlegend=True,
    )
    fig.update_xaxes(title_text="Step", row=1, col=1)
    fig.update_xaxes(title_text="Step", row=2, col=1)
    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="μ Mean", row=2, col=1)

    return fig


def serialize_history(history: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
    """Convert history to fully JSON-safe types."""
    return {
        k: [
            bool(x) if isinstance(x, bool)
            else float(x) if isinstance(x, (np.floating, float))
            else int(x) if isinstance(x, (np.integer, int))
            else x
            for x in v
        ]
        for k, v in history.items()
    }


def export_symbiosis_log(
    history: Dict[str, List[Any]],
    config: SimulationConfig,
    filename: str = "symbiosis_log.json",
) -> Path:
    if not history["coherence"]:
        raise RuntimeError("Cannot export empty history.")

    actions = history["action"]
    action_summary = {
        "inward": int(sum(1 for a in actions if a == "inward")),
        "outward": int(sum(1 for a in actions if a == "outward")),
        "vetoed": int(sum(1 for a in actions if a == "vetoed")),
    }

    log = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "steps": len(history["coherence"]),
        "final_coherence": float(history["coherence"][-1]),
        "min_coherence": float(min(history["coherence"])),
        "max_coherence": float(max(history["coherence"])),
        "mean_coherence": float(np.mean(history["coherence"])),
        "final_mu_mean": float(history["mu_mean"][-1]),
        "mean_mu": float(np.mean(history["mu_mean"])),
        "final_togal_stage": float(history["togal_stage"][-1]),
        "veto_count": int(sum(history["vetoed"])),
        "action_summary": action_summary,
        "config": asdict(config),
        "history": serialize_history(history),
    }

    out_path = Path(filename).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    return out_path


def print_summary(summary: RunSummary) -> None:
    total = max(summary.steps, 1)
    print("Kairos Echo — Simulation Summary")
    print("=" * 45)
    print(f"Timestamp (UTC)     : {summary.timestamp_utc}")
    print(f"Steps               : {summary.steps}")
    print(f"Final coherence     : {summary.final_coherence:.4f}")
    print(
        f"Mean coherence      : {summary.mean_coherence:.4f} "
        f"(min {summary.min_coherence:.4f} / max {summary.max_coherence:.4f})"
    )
    print(
        f"Final μ mean        : {summary.final_mu_mean:.4f} "
        f"(overall mean {summary.mean_mu:.4f})"
    )
    print(f"Final Tögal stage   : {summary.final_togal_stage:.2f}")
    print(
        f"Guardian vetoes     : {summary.veto_count} "
        f"({summary.vetoed_action_count / total * 100:.1f}% of actions)"
    )
    print(
        f"Inward actions      : {summary.inward_count} "
        f"({summary.inward_count / total * 100:.1f}%)"
    )
    print(
        f"Outward actions     : {summary.outward_count} "
        f"({summary.outward_count / total * 100:.1f}%)"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Kairos Echo — Hardened Ethical Coherence Simulator"
    )
    parser.add_argument(
        "--mode",
        choices=["run", "summary", "dashboard", "togal", "trekcho", "log"],
        default="run",
        help="Operation mode",
    )
    parser.add_argument("--steps", type=int, default=300, help="Number of simulation steps")
    parser.add_argument("--size", type=int, default=200, help="μ field size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument(
        "--inward-probability",
        type=float,
        default=0.75,
        help="Probability of inward action",
    )
    parser.add_argument(
        "--save-html",
        type=str,
        default="",
        help="Save dashboard to HTML file (dashboard mode)",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="symbiosis_log.json",
        help="Output path for JSON log",
    )
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()

        config = SimulationConfig(
            size=args.size,
            seed=args.seed,
            steps=args.steps,
            inward_probability=args.inward_probability,
        )

        proto = KairosEchoPrototype(config)
        history = proto.run(reset=True)
        summary = proto.summary()

        if args.mode == "run":
            print_summary(summary)
            print("\n" + generate_togal_reflection(summary.final_coherence, summary.final_togal_stage))
            return 0

        if args.mode == "summary":
            print_summary(summary)
            return 0

        if args.mode == "dashboard":
            fig = plot_togal_visualizer(history)
            if args.save_html:
                path = Path(args.save_html).expanduser().resolve()
                path.parent.mkdir(parents=True, exist_ok=True)
                fig.write_html(str(path))
                print(f"Dashboard saved to: {path}")
            fig.show()
            return 0

        if args.mode == "togal":
            print(generate_togal_reflection(summary.final_coherence, summary.final_togal_stage))
            return 0

        if args.mode == "trekcho":
            print(generate_trekcho_reflection(summary.final_coherence))
            return 0

        if args.mode == "log":
            out_path = export_symbiosis_log(history, config, args.log_file)
            print(f"Symbiosis log exported to: {out_path}")
            return 0

        raise RuntimeError(f"Unhandled mode: {args.mode}")

    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
