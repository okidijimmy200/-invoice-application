import re


def extract_acceptance_scenarios(spec_text: str) -> list[str]:
    scenarios = []
    current_scenario = None

    for line in spec_text.splitlines():
        stripped = line.strip()

        # A Markdown heading ends the current acceptance section/scenario.
        if stripped.startswith("#"):
            if current_scenario:
                scenarios.append(current_scenario)
                current_scenario = None
            continue

        if stripped == "---":
            if current_scenario:
                scenarios.append(current_scenario)
                current_scenario = None
            continue

        # Start of a numbered Given/When/Then scenario.
        match = re.match(r"^\d+\.\s+(\*\*Given\*\*.+)", stripped)

        if match:
            if current_scenario:
                scenarios.append(current_scenario)

            current_scenario = match.group(1)
            continue

        # Continue collecting wrapped scenario text.
        if current_scenario:
            if stripped:
                current_scenario = f"{current_scenario.rstrip()} {stripped.lstrip()}"

    if current_scenario:
        scenarios.append(current_scenario)

    return scenarios

def build_acceptance_requirements(scenarios: list[str]) -> list[dict]:
    requirements = []

    for index, scenario in enumerate(scenarios, start=1):
        requirements.append(
            {
                "id": f"AC-{index:03d}",
                "text": scenario,
            }
        )

    return requirements