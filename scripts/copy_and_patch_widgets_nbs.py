"""
Script to:
- Pull all the reference notebooks from Panel
- Find the widgets that have been implemented in panel-material-ui and have a notebook in Panel
- Prepend a bit of code that monkey patches `pn.widgets`
- Save the notebooks in example/reference/widgets
"""

import os
import shutil
import subprocess

from pathlib import Path

import nbformat
import panel_material_ui as pnmui

PANEL_SPARSE_REF = 'panel_sparse_ref'

if Path(PANEL_SPARSE_REF).exists():
    shutil.rmtree(PANEL_SPARSE_REF)

subprocess.run(f'git clone --depth 1 --filter=blob:none --sparse https://github.com/holoviz/panel.git {PANEL_SPARSE_REF}', shell=True, check=True)
cdir = os.getcwd()
os.chdir(PANEL_SPARSE_REF)
try:
    subprocess.run('git sparse-checkout set examples/reference', shell=True)
finally:
    os.chdir(cdir)

mwidgets = [w.lower() for w in dir(pnmui.widgets)]
nb_to_copy = []

for nb in Path(PANEL_SPARSE_REF, 'examples', 'reference', 'widgets').glob('*.ipynb'):
    if nb.stem.lower() in mwidgets:
        nb_to_copy.append(nb)

for nbpath in nb_to_copy:
    with open(nbpath, "r") as f:
        notebook = nbformat.read(f, as_version=4)
    monkey = nbformat.v4.new_code_cell(source="import panel_material_ui as pnmui; import panel as pn; pn.widgets = pnmui.widgets")
    notebook['cells'].insert(0, monkey)
    opath = Path('examples', 'reference', 'widgets', nbpath.name)
    if opath.exists():
        opath.unlink()
    print(f'Writing {opath}')
    nbformat.write(notebook, opath, version=nbformat.NO_CONVERT)
