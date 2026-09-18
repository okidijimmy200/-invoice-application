from pathlib import Path


def read_spec(spec_file: Path) -> str:
    if not spec_file.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_file}")

    return spec_file.read_text(encoding="utf-8")