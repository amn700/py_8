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

    missing: bool = False
    for dist_name, purpose in REQUIRED_PACKAGES.items():
        ver = _get_version(dist_name)
        if ver is None:
            missing = True
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
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    month = 30
    print(f"Processing {month} data points...")
    meals = np.random.randint(low=2, high=8, size=month)

    df = pd.Series({"meals": meals})
    print(df)
    print("Generating visualization...\n")

    fig, ax = plt.subplots(figsize=(15, 10))

    ax.plot(df["meals"], linewidth=2, label="meal")
    ax.set_title("how many time did i eat this month !")
    ax.set_ylabel("meals")
    ax.set_xlabel("days")
    ax.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig("matrix_analysis.png", dpi=600)
    plt.close(fig)

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    if not print_dependency_status():
        raise SystemExit(1)

    analyze_and_plot()


if __name__ == "__main__":
    main()
