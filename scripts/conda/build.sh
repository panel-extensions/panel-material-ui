#!/usr/bin/env bash

set -euxo pipefail

python -m build --sdist .

SDIST=$(ls dist/panel_material_ui-*.tar.gz | sort -V | tail -n1)
VERSION=$(basename "$SDIST" .tar.gz | sed 's/^panel_material_ui-//')
export VERSION

conda build scripts/conda/recipe --no-anaconda-upload --no-verify -c conda-forge --package-format 2

mv "$CONDA_PREFIX/conda-bld/noarch/panel-material-ui-$VERSION-py_0.conda" dist
