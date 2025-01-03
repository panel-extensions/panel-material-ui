from __future__ import annotations

import inspect
import pathlib

import param
from panel.config import config
from panel.custom import ReactComponent
from panel.util import classproperty

COLORS = ["primary", "secondary", "error", "info", "success", "warning"]


THEME_WRAPPER = """
import {{ ThemeProvider, createTheme }} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

{esm}

function themed_render(props) {{
  const [defaultTheme] = props.model.useState('theme')

  const theme = createTheme({{
    colorSchemes: {{
      dark: defaultTheme === "dark",
    }},
  }});

  return (
    <ThemeProvider theme={{theme}}>
      <CssBaseline />
      <Panel{component} {{...props}}/>
    </ThemeProvider>
  )
}}

export default {{ render: themed_render }}
"""


class MaterialComponent(ReactComponent):

    theme = param.Selector(default="default", objects=["default", "dark"])

    _importmap = {
        "imports": {
            "@mui/material/": "https://esm.sh/@mui/material@6.1.7/",
            "@mui/icons-material/": "https://esm.sh/@mui/icons-material@6.1.7/",
        }
    }

    _esm_base = None

    # _bundle = "panel-material-ui.bundle.js"

    def __init__(self, **params):
        if 'theme' not in params:
            params['theme'] = config.theme
        super().__init__(**params)

    @classproperty
    def _esm(cls):
        if cls._esm_base is None:
            return None
        esm_base = pathlib.Path(inspect.getfile(cls)).parent / cls._esm_base
        component = cls.__name__
        esm = (
            esm_base
            .read_text()
            .replace('export function render(', f'export function Panel{component}(')
            .replace('const render =', f'const Panel{component} =')
        )
        return THEME_WRAPPER.format(esm=esm, component=component)

    __abstract = True
