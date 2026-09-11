from pathlib import Path


def register(ctx):
    for name in (
        "qawolf",
        "qawolf-flow-maintenance",
        "qawolf-flow-outline",
        "qawolf-onboarding",
    ):
        ctx.register_skill(name, Path(__file__).parent / "skills" / name / "SKILL.md")
