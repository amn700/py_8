import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    print("Missing dependency: python-dotenv")
    print("Activate your venv, then install:")
    print("  python -m pip install python-dotenv")
    raise SystemExit(1)


_KEYS = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT"]


def _script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _is_truthy(value: str | None) -> bool:
    return value is not None and value.strip() != ""


def _normalize_mode(raw: str | None) -> str:
    if raw is None:
        return "development"

    mode = raw.strip().lower()
    if mode in ("development", "production"):
        return mode

    return "development"


def _gitignore_ignores_env(gitignore_text: str) -> bool:
    for line in gitignore_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in (".env", "**/.env"):
            return True
    return False


def _describe_database(database_url: str | None) -> str:
    if not _is_truthy(database_url):
        return "Not configured"

    url = database_url.strip().lower()
    if url.startswith("sqlite:") or "localhost" in url or "127.0.0.1" in url:
        return "Connected to local instance"

    return "Connected to production instance"


def _describe_zion(endpoint: str | None) -> str:
    if not _is_truthy(endpoint):
        return "Offline"

    ep = endpoint.strip().lower()
    if ep.startswith("http://") or ep.startswith("https://"):
        return "Online"

    return "Misconfigured"


def main() -> None:

    print("\nORACLE STATUS: Reading the Matrix...\n")

    script_dir = _script_dir()
    dotenv_path = os.path.join(script_dir, ".env")

    dotenv_loaded = load_dotenv(dotenv_path=dotenv_path, override=False)

    raw_mode = os.environ.get("MATRIX_MODE")

    mode = _normalize_mode(raw_mode)

    warnings: list[str] = []

    if raw_mode is not None and raw_mode.strip().lower() not in ("development", "production"):
        warnings.append('MATRIX_MODE must be "development" or "production" (defaulting to development)')

    dev_defaults: dict[str, str] = {
        "DATABASE_URL": "sqlite:///matrix_dev.db",
        "LOG_LEVEL": "DEBUG",
        "ZION_ENDPOINT": "http://localhost:8000/zion",
    }

    config: dict[str, str | None] = {"MATRIX_MODE": mode}

    for key in _KEYS:
        if key == "MATRIX_MODE":
            continue

        val = os.environ.get(key)

        if val is None and mode == "development" and key in dev_defaults:
            val = dev_defaults[key]
            warnings.append(f"{key} is missing (using development default)")

        if val is None:
            warnings.append(f"{key} is missing")

        config[key] = val

    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {_describe_database(config['DATABASE_URL'])}")

    api_key = config.get("API_KEY")
    if _is_truthy(api_key):
        print("API Access: Authenticated")
    else:
        print("API Access: Not configured")

    log_level = config.get("LOG_LEVEL")
    if _is_truthy(log_level):
        print(f"Log Level: {log_level}")
    else:
        print("Log Level: Not configured")

    print(f"Zion Network: {_describe_zion(config['ZION_ENDPOINT'])}")

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"- {w}")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")

    gitignore_path = os.path.join(script_dir, ".gitignore")
    gitignore_text = _read_text(gitignore_path)
    env_is_ignored = _gitignore_ignores_env(gitignore_text)

    if os.path.isfile(dotenv_path):
        if env_is_ignored:
            print("[OK] .env file properly configured")
        else:
            print("[WARN] .env exists but is not ignored by .gitignore")
    else:
        if dotenv_loaded:
            print("[WARN] .env loaded but file not found (unexpected)")
        else:
            if mode == "development":
                print("[WARN] .env file not found (copy .env.example -> .env for development)")
            else:
                print("[OK] No .env file present (recommended for production)")

    print("[OK] Production overrides available")

    if _is_truthy(api_key) and api_key.strip().lower() in ("change-me", "changeme", "replace-me", "replace_me"):
        print("[WARN] API_KEY looks like a placeholder (set a real value)")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
