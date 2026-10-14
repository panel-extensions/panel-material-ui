from __future__ import annotations

import os
import shutil
import subprocess
import sys
import typing as t

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

BASE_DIR = Path(__file__).parent
GREEN, RED, RESET = "\033[0;32m", "\033[0;31m", "\033[0m"


def compile_bundle():
    print(f"{GREEN}[PANEL-MATERIAL-UI]{RESET} Compile panel-material-ui bundle", flush=True)

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if npm is None:
        print(f"{RED}[PANEL-MATERIAL-UI]{RESET} npm is required to build the bundle", flush=True)
        sys.exit(1)
    try:
        if not (BASE_DIR / "node_modules").is_dir():
            subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=BASE_DIR, check=True)
        subprocess.run([npm, "run", "build"], cwd=BASE_DIR, check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}[PANEL-MATERIAL-UI]{RESET} Failed building bundle", flush=True)
        sys.exit(1)
    finally:
        if sys.platform != "win32":
            # npm can cause non-blocking stdout; so reset it just in case
            import fcntl

            flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL)
            fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)

    subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "generate_font_css.py")],
        cwd=BASE_DIR,
        check=True,
    )
    print(f"{GREEN}[PANEL-MATERIAL-UI]{RESET} Finished building bundle", flush=True)


class BuildHook(BuildHookInterface):
    """The hatch build hook."""

    PLUGIN_NAME = "install"

    def initialize(self, version: str, build_data: dict[str, t.Any]) -> None:
        """Initialize the plugin."""
        if self.target_name not in ["wheel", "sdist"]:
            return

        if os.environ.get("PANEL_MATERIAL_UI_SKIP_COMPILE"):
            # Used by the conda recipe, which installs from an sdist that
            # already ships the compiled JS bundle, and whose isolated
            # build environment does not have panel/nodejs available.
            return

        compile_bundle()
