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

from param import concrete_descendents

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
mwidgets = list(concrete_descendents(pnmui.widgets.base.MaterialWidget))
nb_to_copy = []
mwidgets_not_implemented = []

for nb in Path(PANEL_SPARSE_REF, 'examples', 'reference', 'widgets').glob('*.ipynb'):
    if nb.stem in mwidgets:
        nb_to_copy.append(nb)
        mwidgets.remove(nb.stem)
    else:
        mwidgets_not_implemented.append(nb.stem)

print(f'These Material widgets have no reference notebook in Panel:\n{"\n".join(sorted(mwidgets))}')
print()
print(f'These Panel widgets have no Material implementation:\n{"\n".join(sorted(mwidgets_not_implemented))}')
print()

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
