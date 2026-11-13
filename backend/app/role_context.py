from __future__ import annotations

from pathlib import Path


class RoleContextReference:
    def __init__(self, profiles_path: str | Path):
        self.profiles_path = Path(profiles_path)

    def build(self, profile_id: str | None) -> dict | None:
        if not profile_id:
            return None

        full_profile = self.full_profile(profile_id)
        if full_profile is None:
            return None

        role_name = self._line_value(full_profile, "Role Name")
        context = {
            "profile_id": profile_id,
            "role_name": role_name,
            "role_intent": self._line_value(full_profile, "Role Intent"),
            "responsibility_boundary": self._section(full_profile, "Responsibility Boundary"),
            "expected_output_shape": self._section(full_profile, "Expected Output Shape"),
            "escalation_triggers": self._section(full_profile, "Escalation Triggers"),
            "source_references": self._section(full_profile, "Source References"),
        }
        context["context_excerpt"] = self._format_excerpt(context)
        return context

    def full_profile(self, profile_id: str | None) -> str | None:
        if not profile_id or not self.profiles_path.exists():
            return None

        content = self.profiles_path.read_text(encoding="utf-8")
        blocks = content.split("\n## Profile: ")
        for block in blocks[1:]:
            profile = "## Profile: " + block
            profile = profile.split("\n## Profile: ", 1)[0]
            profile = profile.split("\n## Determinism Rules", 1)[0].rstrip()
            if f"Stable Profile ID: `{profile_id}`" in profile:
                return profile
        return None

    @staticmethod
    def _line_value(text: str, label: str) -> str:
        prefix = f"{label}: "
        for line in text.splitlines():
            if line.startswith(prefix):
                return line.removeprefix(prefix).strip()
        return ""

    @staticmethod
    def _section(text: str, heading: str) -> str:
        marker = f"{heading}:"
        lines = text.splitlines()
        try:
            start = lines.index(marker) + 1
        except ValueError:
            return ""

        collected: list[str] = []
        for line in lines[start:]:
            if line.endswith(":") and collected:
                break
            if line.startswith("## "):
                break
            if line.strip():
                collected.append(line.strip())
        return "\n".join(collected)

    @staticmethod
    def _format_excerpt(context: dict) -> str:
        return "\n".join(
            [
                f"Role Profile: {context['profile_id']} ({context['role_name']})",
                f"Role Intent: {context['role_intent']}",
                "Responsibility Boundary:",
                context["responsibility_boundary"],
                "Expected Output Shape:",
                context["expected_output_shape"],
                "Escalation Triggers:",
                context["escalation_triggers"],
                "Source References:",
                context["source_references"],
            ]
        )
