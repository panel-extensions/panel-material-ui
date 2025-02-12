from __future__ import annotations

import inspect
import pathlib
import textwrap
from typing import Literal

import param
from panel.config import config
from panel.custom import ReactComponent
from panel.util import base_version, classproperty

from .__version import __version__  # noqa
from .theme import MaterialDesign

COLORS = ["primary", "secondary", "error", "info", "success", "warning"]

BASE_PATH = pathlib.Path(__file__).parent
CDN_DIST = "https://cdn.holoviz.org/panel-material-ui/v{__version__}/panel-material-ui.bundle.js"


class ESMTransform:
    """
    ESMTransform allows writing transforms for ReactComponent
    that add additional functionality by wrapping the base
    ESM with a wrapping function.
    """

    _transform: str | None = None

    @classmethod
    def apply(cls, component: type[ReactComponent], esm: str, input_component: str) -> tuple[str, str]:
        name = cls.__name__.replace('Transform', '')
        output = f'{name}{component.__name__}'
        return cls._transform.format(
            esm=esm,
            input=input_component,
            output=output
        ), output


class ThemedTransform(ESMTransform):

    _transform = """\
import * as React from "react"
import 'material-icons/iconfont/material-icons.css';
import {{ ThemeProvider, createTheme }} from '@mui/material/styles';
import {{ deepmerge }} from '@mui/utils';
import CssBaseline from '@mui/material/CssBaseline';

{esm}

function {output}(props) {{
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
      <{input} {{...props}}/>
    </ThemeProvider>
  )
}}
"""


class MaterialComponent(ReactComponent):
    """
    Baseclass for all MaterialComponents which defines the bundle location,
    the JS dependencies and theming support via the ThemedTransform.
    """

    dark_theme = param.Boolean()

    theme_config = param.Dict(default=None, nested_refs=True, doc="Options to configure the ThemeProvider")

    _bundle = BASE_PATH / "dist" / "panel-material-ui.bundle.js"
    _esm_base = None
    _esm_transforms = [ThemedTransform]
    _importmap = {
        "imports": {
            "@mui/icons-material/": "https://esm.sh/@mui/icons-material@6.4.2/",
            "@mui/material/": "https://esm.sh/@mui/material@6.4.2/",
            "@mui/x-date-pickers/": "https://esm.sh/@mui/x-date-pickers@7.24.1",
            "dayjs": "https://esm.sh/dayjs@1.11.5",
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
            return [str(css_path)] + [str(p) for p in (BASE_PATH / 'dist').glob('material-icons-*.woff*')]
        return []

    @classmethod
    def _render_esm_base(cls):
        esm_base = (pathlib.Path(inspect.getfile(cls)).parent / cls._esm_base).read_text()
        if not cls._esm_transforms:
            return esm_base

        component_name = f'Panel{cls.__name__}'
        esm_base = esm_base.replace('export function render', f'function {component_name}')
        for transform in cls._esm_transforms:
            esm_base, component_name = transform.apply(cls, esm_base, component_name)
        esm_base += f'\nexport default {{ render: {component_name} }}'
        return textwrap.dedent(esm_base)

    @classmethod
    def _render_esm(cls, compiled: bool | Literal['compiling'] = True, server: bool = False):
        if compiled != 'compiling':
            if compiled and __version__ == base_version(__version__):
                return CDN_DIST
            else:
                return super()._render_esm(compiled=True, server=server)
        elif cls._esm_base is None:
            return None
        return cls._render_esm_base()
