#!/usr/bin/env bash

set -euxo pipefail

python -m build --sdist .

VERSION=$(python -c "import panel_material_ui; print(panel_material_ui.__version__)")
export VERSION

conda build scripts/conda/recipe --no-anaconda-upload --no-verify -c conda-forge --package-format 2

mv "$CONDA_PREFIX/conda-bld/noarch/panel-material-ui-$VERSION-py_0.conda" dist
