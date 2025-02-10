from __future__ import annotations

import inspect
import pathlib
import textwrap
from typing import Literal

import param
from panel.config import config
from panel.custom import ReactComponent
from panel.util import classproperty

from .theme import MaterialDesign

COLORS = ["primary", "secondary", "error", "info", "success", "warning"]

BASE_PATH = pathlib.Path(__file__).parent

THEME_WRAPPER = """\
import 'material-icons/iconfont/material-icons.css';
import {{ ThemeProvider, createTheme }} from '@mui/material/styles';
import {{ deepmerge }} from '@mui/utils';
import CssBaseline from '@mui/material/CssBaseline';

{esm}

function themed_render(props) {{
  const [dark_theme] = props.model.useState('dark_theme')
  const [theme_config ] = props.model.useState('theme_config')

  const config = deepmerge(
    theme_config,
    {{
      cssVariables: {{
        rootSelector: ':host',
        colorSchemeSelector: 'class',
      }},
      palette: {{
        mode: dark_theme ? "dark" : "light"
      }},
      components: {{
        MuiPopover: {{
          defaultProps: {{
            container: props.view.container,
          }},
        }},
        MuiPopper: {{
          defaultProps: {{
            container: props.view.container,
          }},
        }},
        MuiModal: {{
          defaultProps: {{
            container: props.view.container,
          }},
        }},
      }}
    }}
  )
  const theme = createTheme(config);

  React.useEffect(() => {{
    let styleElement = document.querySelector("#global-styles-panel-mui");
    if (!styleElement) {{
      styleElement = document.createElement("style");
      styleElement.id = "global-styles-panel-mui";
      document.head.appendChild(styleElement)
    }}

    styleElement.textContent = `
      :root, :host {{
        --panel-primary-color: ${{theme.palette.primary.main}};
        --panel-on-primary-color: ${{theme.palette.primary.contrastText}};
        --panel-secondary-color: ${{theme.palette.secondary.main}};
        --panel-on-secondary-color: ${{theme.palette.secondary.contrastText}};
        --panel-background-color: ${{theme.palette.background.default}};
        --panel-on-background-color: ${{theme.palette.text.primary}};
        --panel-surface-color: ${{theme.palette.background.paper}};
        --panel-on-surface-color: ${{theme.palette.text.primary}};
      }}
    `;

  }}, [theme]);

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

    dark_theme = param.Boolean()

    theme_config = param.Dict(default=None, nested_refs=True, doc="Options to configure the ThemeProvider")

    _bundle = BASE_PATH / "panel-material-ui.bundle.js"
    _esm_base = None
    _importmap = {
        "imports": {
            "@mui/icons-material/": "https://esm.sh/@mui/icons-material@6.4.2/",
            "@mui/material/": "https://esm.sh/@mui/material@6.4.2/",
            "@mui/x-date-pickers/": "https://esm.sh/@mui/x-date-pickers@7.24.1",
            "luxon": "https://esm.sh/luxon@3",
            "material-icons/": "https://esm.sh/material-icons@1.13.13/"
        }
    }

    __abstract = True

    def __init__(self, **params):
        if 'dark_theme' not in params:
            params['dark_theme'] = config.theme == 'dark'
        if 'design' not in params:
            params['design'] = MaterialDesign
        super().__init__(**params)

    async def _watch_esm(self):
        import watchfiles
        async for _ in watchfiles.awatch(self._bundle, stop_event=self._watching_esm):
            self._update_esm()

    @classmethod
    def _esm_path(cls, compiled=True):
        if compiled != 'compiling':
            return cls._bundle_path
        if hasattr(cls, '__path__'):
            mod_path = cls.__path__
        else:
            mod_path = pathlib.Path(inspect.getfile(cls)).parent
        esm_path = mod_path / cls._esm_base
        return esm_path

    @classproperty
    def _bundle_css(cls):
        esm_path = cls._esm_path(compiled=True)
        css_path = esm_path.with_suffix('.css')
        if css_path.is_file():
            return [str(css_path)] + [str(p) for p in BASE_PATH.glob('material-icons-*.woff*')]
        return []

    @classmethod
    def _render_esm(cls, compiled: bool | Literal['compiling'] = True, server: bool = False):
        if compiled != 'compiling':
            return super()._render_esm(compiled=compiled, server=server)
        elif cls._esm_base is None:
            return None
        esm_base = pathlib.Path(inspect.getfile(cls)).parent / cls._esm_base
        component = cls.__name__
        esm = (
            esm_base
            .read_text()
            .replace('export function render(', f'export function Panel{component}(')
            .replace('const render =', f'const Panel{component} =')
        )
        esm = textwrap.dedent(esm)
        if compiled == 'compiling':
            esm = 'import * as React from "react"\n' + esm
        wrapper = THEME_WRAPPER.format(esm=esm, component=component)
        return wrapper
