import os
import json

bundle_path = "src/panel_material_ui/dist/panel-material-ui.bundle.js"
if not os.path.isfile(bundle_path):
    raise FileNotFoundError(f"Could not find file: {bundle_path}")

size_bytes = os.path.getsize(bundle_path)

size_report = {
    "files": [
        {
            "name": "panel-material-ui.bundle.js",
            "path": bundle_path,
            "size": size_bytes
        }
    ]
}

with open("size.json", "w") as f:
    json.dump(size_report, f, indent=2)

print("✅ size.json generated:")
print(json.dumps(size_report, indent=2))
