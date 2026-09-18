from pathlib import Path
from spec_reader import read_spec
from planner import plan_verification
from requirement_extractor import (
    extract_acceptance_scenarios,
    build_acceptance_requirements,
)


def discover_project(project_root: Path) -> dict:
    return {
        "project_root": project_root,
        "spec_dir": project_root / "specs" / "001-invoice-management",
        "spec_file": project_root / "specs" / "001-invoice-management" / "spec.md",
        "plan_file": project_root / "specs" / "001-invoice-management" / "plan.md",
        "tasks_file": project_root / "specs" / "001-invoice-management" / "tasks.md",
        "openapi_file": project_root
        / "specs"
        / "001-invoice-management"
        / "contracts"
        / "openapi.yaml",
        "backend_dir": project_root / "backend",
        "frontend_dir": project_root / "frontend",
    }


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    project = discover_project(project_root)

    for name, path in project.items():
        exists = path.exists()
        status = "FOUND" if exists else "MISSING"
        print(f"[{status}] {name}: {path}")

    spec_text = read_spec(project["spec_file"])

    print("\n--- SPEC PREVIEW ---")
    print(spec_text[:1000])

    scenarios = extract_acceptance_scenarios(spec_text)

    print("\n--- ACCEPTANCE SCENARIOS ---")
    for index, scenario in enumerate(scenarios, start=1):
        print(f"{index}. {scenario}")

    requirements = build_acceptance_requirements(scenarios)
    

    print("\n--- STRUCTURED REQUIREMENTS ---")
    for requirement in requirements:
        print(f"{requirement['id']}: {requirement['text']}")

    ac_003 = next(
    requirement
    for requirement in requirements
    if requirement["id"] == "AC-003"
)

    obligations = plan_verification(ac_003)

    print("\n--- VERIFICATION OBLIGATIONS ---")
    for obligation in obligations:
        print(
            f"{obligation.id} | "
            f"{obligation.requirement_id} | "
            f"{obligation.method} | "
            f"{obligation.description}"
        )