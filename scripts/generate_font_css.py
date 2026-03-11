from pathlib import Path
import re
import sys

DIST_PATH = Path(__file__).parent.parent / "src" / "panel_material_ui" / "dist"

FONT_FAMILY_MAP = {
    "material-icons": "Material Icons",
    "material-icons-outlined": "Material Icons Outlined",
    "roboto": "Roboto",
    "roboto-math": "Roboto Math",
    "roboto-symbols": "Roboto Symbols",
}

WEIGHT_MAP = {
    "normal": "normal",
    "italic": "italic",
}

UNICODE_RANGE_MAP = {
    ("roboto", "latin-ext"): "U+0100-024F",
}

PATTERNS = [
    re.compile(r"^(?P<family>material-icons-outlined)-(?P<hash>[A-Z0-9]+)\.(?P<ext>woff2?|ttf|otf)$"),
    re.compile(r"^(?P<family>material-icons)-(?P<hash>[A-Z0-9]+)\.(?P<ext>woff2?|ttf|otf)$"),
    re.compile(
        r"^(?P<family>roboto(?:-math|-symbols)?)-(?P<subset>[a-z0-9-]+)-(?P<weight>\d+)-(?P<style>normal|italic)-(?P<hash>[A-Z0-9]+)\.(?P<ext>woff2?|ttf|otf)$"
    ),
]

FORMAT_MAP = {
    "woff2": "woff2",
    "woff": "woff",
    "ttf": "truetype",
    "otf": "opentype",
}

EXT_PRIORITY = {
    "woff2": 0,
    "woff": 1,
    "otf": 2,
    "ttf": 3,
}

SUBSET_PRIORITY = {
    "latin": 0,
    "latin-ext": 1,
}

def parse_file(path: Path):
    name = path.name
    for pattern in PATTERNS:
        match = pattern.match(name)
        if not match:
            continue
        data = match.groupdict()
        family_key = data["family"]
        if family_key.startswith("material-icons"):
            return {
                "family_key": family_key,
                "family_name": FONT_FAMILY_MAP[family_key],
                "subset": None,
                "weight": "400",
                "style": "normal",
                "ext": data["ext"],
                "file": name,
            }
        return {
            "family_key": family_key,
            "family_name": FONT_FAMILY_MAP[family_key],
            "subset": data["subset"],
            "weight": data["weight"],
            "style": data["style"],
            "ext": data["ext"],
            "file": name,
        }
    return None

def sort_src(entries):
    return sorted(entries, key=lambda e: (EXT_PRIORITY.get(e["ext"], 99), e["file"]))

def block_key(item):
    subset_rank = SUBSET_PRIORITY.get(item["subset"], 99) if item["subset"] is not None else -1
    return (item["family_name"], int(item["weight"]), item["style"], subset_rank, item["subset"] or "")

def generate_css(directory: Path):
    parsed = []
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"}:
            item = parse_file(path)
            if item:
                parsed.append(item)

    groups = {}
    for item in parsed:
        key = (item["family_name"], item["family_key"], item["subset"], item["weight"], item["style"])
        groups.setdefault(key, []).append(item)

    blocks = []
    for key in sorted(groups.keys(), key=lambda k: block_key({
        "family_name": k[0],
        "subset": k[2],
        "weight": k[3],
        "style": k[4],
    })):
        family_name, family_key, subset, weight, style = key
        entries = sort_src(groups[key])
        lines = ["@font-face {", f'  font-family: "{family_name}";']
        src_parts = [f'url("./{entry["file"]}") format("{FORMAT_MAP[entry["ext"]]}")' for entry in entries]
        if src_parts:
            lines.append("  src: " + ",\n       ".join(src_parts) + ";")
        if family_key.startswith("material-icons"):
            lines.append("  font-weight: normal;")
            lines.append("  font-style: normal;")
        else:
            lines.append(f"  font-weight: {weight};")
            lines.append(f"  font-style: {style};")
            unicode_range = UNICODE_RANGE_MAP.get((family_key, subset))
            if unicode_range:
                lines.append(f"  unicode-range: {unicode_range};")
        lines.append("}")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks) + ("\n" if blocks else "")

def main():
    css_path = DIST_PATH / "material-icons.css"
    css = generate_css(DIST_PATH)
    css_path.write_text(css, encoding="utf-8")
    print(css_path)

if __name__ == "__main__":
    main()
