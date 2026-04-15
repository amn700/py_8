from importlib import metadata

REQUIRED_PACKAGES = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}


def _get_version(dist_name: str) -> str | None:
    try:
        return metadata.version(dist_name)
    except metadata.PackageNotFoundError:
        return None


def print_dependency_status() -> bool:
    print("\nLOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    missing: list[str] = []
    for dist_name, purpose in REQUIRED_PACKAGES.items():
        ver = _get_version(dist_name)
        if ver is None:
            missing.append(dist_name)
            print(f"[MISSING] {dist_name} - {purpose} not available")
        else:
            print(f"[OK] {dist_name} ({ver}) - {purpose} ready")

    if missing:
        print("Missing dependencies detected.")
        print("Install with pip:")
        print("  python -m pip install -r requirements.txt")
        print("Or install with Poetry:")
        print("  poetry install")
        print("  poetry run python loading.py")
        return False

    return True


def analyze_and_plot() -> None:
    import matplotlib
    import numpy as np
    import pandas as pd

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    points = 1000
    print(f"Processing {points} data points...")

    rng = np.random.default_rng(42)
    tick = np.arange(points)
    base = 50.0 + 10.0 * np.sin(tick / 40.0)
    noise = rng.normal(loc=0.0, scale=2.0, size=points)
    signal = base + noise

    spike_idx = rng.choice(points, size=10, replace=False)
    signal[spike_idx] += rng.normal(loc=20.0, scale=5.0, size=10)

    df = pd.DataFrame({"tick": tick, "signal": signal})
    df["rolling_mean"] = df["signal"].rolling(window=50, min_periods=1).mean()

    print("Generating visualization...\n")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["tick"], df["signal"], alpha=0.35, linewidth=1, label="raw signal")
    ax.plot(df["tick"], df["rolling_mean"], linewidth=2, label="rolling mean (50)")

    ax.set_title("Simulated Matrix signal (1000 points)")
    ax.set_xlabel("tick")
    ax.set_ylabel("signal")
    ax.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig("matrix_analysis.png", dpi=150)
    plt.close(fig)

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    if not print_dependency_status():
        raise SystemExit(1)

    analyze_and_plot()


if __name__ == "__main__":
    main()
