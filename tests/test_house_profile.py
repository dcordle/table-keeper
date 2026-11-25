"""table-keeper campaign profiles: the checker in skills/shared/house.

Run: python3 -m pytest tests/test_house_profile.py -q
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSE = ROOT / "skills" / "shared" / "house"
_spec = importlib.util.spec_from_file_location("profile_check", HOUSE / "profile_check.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

TEMPLATE = (HOUSE / "profile-template.md").read_text(encoding="utf-8")


def test_the_template_passes():
    assert pc.check_text(TEMPLATE) == []


def test_bands():
    assert pc.band_error("> Moderate and <= High") is None
    assert pc.band_error(">= 1.5x High") is None
    assert pc.band_error("judgment") is None
    assert pc.band_error("above Moderate") is not None
    assert pc.band_error("> Moderate and") is not None


def test_a_bad_value_is_named():
    bad = TEMPLATE.replace("**Format:** open table", "**Format:** West Marches")
    assert any("'Format' is 'West Marches'" in p for p in pc.check_text(bad))


def test_a_missing_required_field_is_named():
    bad = TEMPLATE.replace("- **Story center:** world\n", "")
    assert "Table: missing field 'Story center'" in pc.check_text(bad)


def test_an_optional_field_may_be_left_out():
    ok = TEMPLATE.replace("- **Start and end:** the party's base\n", "")
    assert pc.check_text(ok) == []


def test_a_missing_section_is_named():
    bad = TEMPLATE.split("## Voice")[0]
    assert "missing section '## Voice'" in pc.check_text(bad)


def test_an_unknown_field_is_named():
    bad = TEMPLATE.replace("## Travel\n", "## Travel\n\n- **Speed:** fast\n")
    assert "Travel: unknown field 'Speed'" in pc.check_text(bad)


def test_overrides_section_is_allowed():
    ok = TEMPLATE + "\n## Overrides\n\n- **The world:** also after downtime.\n"
    assert pc.check_text(ok) == []


def test_the_title_is_required():
    bad = TEMPLATE.replace("# Table-Keeper Profile: Campaign Name", "# Profile")
    assert any("title must be" in p for p in pc.check_text(bad))


def test_hit_points():
    assert pc._hp("75%") is None
    assert pc._hp("as written") is None
    assert pc._hp("150%") is not None


def test_creative_lead_is_optional_and_checked():
    ok = TEMPLATE.replace("- **Session unit:**", "- **Creative lead:** shared\n- **Session unit:**")
    assert pc.check_text(ok) == []
    bad = TEMPLATE.replace("- **Session unit:**", "- **Creative lead:** player\n- **Session unit:**")
    assert any("'Creative lead' is 'player'" in p for p in pc.check_text(bad))


def test_a_risk_note_may_name_its_levels():
    assert pc._risk("yes") is None
    assert pc._risk("yes, at the tier's lowest, one-up and highest level") is None
    assert pc._risk("no") is None
    assert pc._risk("yes,") is not None
    assert pc._risk("sometimes") is not None


def test_reference_section_is_optional_and_checked():
    ok = TEMPLATE + "\n## Reference\n\n- **Rules source:** supabase\n- **Transcripts:** uploaded in chat\n"
    assert pc.check_text(ok) == []
    missing = TEMPLATE + "\n## Reference\n\n- **Transcripts:** uploaded in chat\n"
    assert "Reference: missing field 'Rules source'" in pc.check_text(missing)
    unknown = TEMPLATE + "\n## Reference\n\n- **Rules source:** none\n- **Password:** x\n"
    assert "Reference: unknown field 'Password'" in pc.check_text(unknown)


def test_rumors_may_be_optional():
    assert pc._rumors("optional") is None
    assert pc._rumors("0") is None and pc._rumors("5") is None
    assert pc._rumors("none required") is not None
