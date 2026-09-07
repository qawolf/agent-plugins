from pathlib import Path


def register(ctx):
    ctx.register_skill(
        "qawolf",
        Path(__file__).parent / "skills" / "qawolf" / "SKILL.md",
    )
