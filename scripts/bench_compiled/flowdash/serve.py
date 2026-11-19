"""Serves a FlowDash project with its tile grid opted into compilation.

    PMUI_COMPILE=0 python serve.py serve <project> --port 5131   # classic
    PMUI_COMPILE=1 python serve.py serve <project> --port 5132   # compiled
"""
import sys

from panel_flowdash.command import main
from panel_tiles import TileGrid

from panel_material_ui.compiler import register

register(TileGrid)
sys.argv = ["flowdash", *sys.argv[1:]]
main()
