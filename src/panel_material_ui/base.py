"""
Panel Material UI is a library that provides Material UI components for Panel.

It implements a collection of widgets and components that follow Material Design
principles and guidelines, providing a modern and consistent look and feel.
The library integrates seamlessly with Panel's reactive programming model while
leveraging the robust Material UI React component library.

The base module provides core functionality including:

- ESM transformation utilities for React components
- Theme configuration and management
- Color constants and configuration
- Base component classes
"""
from __future__ import annotations

import inspect
import pathlib
import textwrap
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

import param
from bokeh.settings import settings as _settings
from panel.config import config
from panel.custom import ReactComponent
from panel.models import ReactComponent as BkReactComponent
from panel.param import Param
from panel.util import base_version, classproperty
from panel.viewable import Viewable

from .__version import __version__  # noqa
from .theme import MaterialDesign

if TYPE_CHECKING:
    from bokeh.document import Document
    from bokeh.model import Model
    from pyviz_comms import Comm

COLORS = ["default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", "danger"]

COLOR_ALIASES = {"danger": "error"}

BASE_PATH = pathlib.Path(__file__).parent
IS_RELEASE = __version__ == base_version(__version__)
CDN_DIST = f"https://cdn.holoviz.org/panel-material-ui/v{base_version(__version__)}/panel-material-ui.bundle.js"


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
    """
    ThemedTransform is a transform that applies a theme to a component.
    It adds a ThemeProvider and CssBaseline to the component.
    """

    _transform = """\
import * as React from "react"
import 'material-icons/iconfont/material-icons.css';
import {{ ThemeProvider, createTheme }} from '@mui/material/styles';
import {{ deepmerge }} from '@mui/utils';
import CssBaseline from '@mui/material/CssBaseline';
import {{SessionStore, dark_mode, render_theme_config, render_theme_css}} from "./utils"

{esm}

function {output}(props) {{
  const [dark_theme, setDarkTheme] = props.model.useState('dark_theme')
  const [theme_config] = props.model.useState('theme_config')

  const config = render_theme_config(props, theme_config, dark_theme)
  const theme = createTheme(config)

  React.useEffect(() => {{
    if (dark_mode.get_value() === dark_theme) {{
      return
    }}
    dark_mode.set_value(dark_theme)
  }}, [dark_theme])

  React.useEffect(() => {{
    let style_el = document.querySelector("#global-styles-panel-mui")
    if (style_el) {{
      return dark_mode.subscribe((val) => setDarkTheme(val))
    }} else {{
      style_el = document.createElement("style")
      style_el.id = "styles-panel-mui"
      props.view.shadow_el.insertBefore(style_el, props.view.container)
      style_el.textContent = render_theme_css(theme)
    }}
  }}, [])

  React.useEffect(() => {{
    const style_el = props.view.shadow_el.querySelector("#styles-panel-mui")
    if (style_el) {{
      style_el.textContent = render_theme_css(theme)
    }}
  }}, [theme])

  return (
    <ThemeProvider theme={{theme}}>
      <CssBaseline />
      <{input} {{...props}}/>
    </ThemeProvider>
  )
}}
"""


class LoadingTransform(ESMTransform):

    _transform = """\
import MuiCircularProgress from '@mui/material/CircularProgress'
import {{ useTheme as useMuiTheme }} from '@mui/material/styles'

{esm}

function {output}(props) {{
  const [loading] = props.model.useState('loading')
  const theme = useMuiTheme()
  if (!loading) {{
    return <{input} {{...props}}/>
  }}

  const overlayColor = theme.palette.mode === 'dark'
    ? 'rgba(0, 0, 0, 0.7)'
    : 'rgba(255, 255, 255, 0.5)'

  return (
    <div style={{{{ position: 'relative' }}}}>
      <{input} {{...props}}/>
      {{loading && (
        <div style={{{{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: overlayColor,
          zIndex: theme.zIndex.modal - 1
        }}}}>
          <MuiCircularProgress color="primary" />
        </div>
      )}}
    </div>
  )
}}"""


class MaterialComponent(ReactComponent):
    """
    Baseclass for all MaterialComponents which defines the bundle location,
    the JS dependencies and theming support via the ThemedTransform.
    """

    dark_theme = param.Boolean(doc="""
        Whether to use dark theme. If not specified, will default to Panel's
        global theme setting.""")

    loading = param.Boolean(default=False, doc="""
        Displays loading spinner on top of the component.""")

    theme_config = param.Dict(default=None, nested_refs=True, doc="""
        Options to configure the ThemeProvider.
        See https://mui.com/material-ui/customization/theme-overview/ for more information.""")

    sx = param.Dict(default=None, doc="""
        A dictionary of CSS styles to apply to the component.
        The keys are the CSS class names and the values are the styles.
        The CSS class names are generated by the component and can be found
        in the component's documentation.""")

    _bundle = BASE_PATH / "dist" / "panel-material-ui.bundle.js"
    _esm_base = None
    _esm_shared = {'utils': BASE_PATH / "utils.js"}
    _esm_transforms = [LoadingTransform, ThemedTransform]
    _importmap = {
        "imports": {
            "@mui/icons-material/": "https://esm.sh/@mui/icons-material@6.4.9/",
            "@mui/material/": "https://esm.sh/@mui/material@6.4.9/",
            "@mui/x-date-pickers/": "https://esm.sh/@mui/x-date-pickers@7.28.0",
            "mui-color-input": "https://esm.sh/mui-color-input@6.0.0",
            "dayjs": "https://esm.sh/dayjs@1.11.5",
            "material-icons/": "https://esm.sh/material-icons@1.13.14/",
            "notistack": "https://esm.sh/notistack@3.0.2"
        }
    }
    _rename = {'loading': 'loading'}

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
        if not config.autoreload and (not config.inline or (IS_RELEASE and _settings.resources(default='server') == 'cdn')):
            return [CDN_DIST.replace('.js', '.css')]
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
        if cls._esm_base is None:
            return None
        elif compiled == 'compiling':
            return cls._render_esm_base()
        elif not config.autoreload and (not (config.inline or server) or (IS_RELEASE and _settings.resources(default='server') == 'cdn')):
            return CDN_DIST
        return super()._render_esm(compiled=True, server=server)

    def _get_model(
        self, doc: Document, root: Model | None = None,
        parent: Model | None = None, comm: Comm | None = None
    ) -> Model:
        model = super()._get_model(doc, root, parent, comm)
        # Ensure model loads ESM and CSS bundles from CDN
        # if requested or if in notebook
        if (
            (comm is None and not config.autoreload and IS_RELEASE and _settings.resources(default='server') == 'cdn') or
            (comm and not config.inline)
        ):
            model.update(
                bundle='url',
                css_bundle=CDN_DIST.replace('.js', '.css'),
                esm=CDN_DIST,
            )
        return model

    def _process_param_change(self, params):
        if 'color' in params:
            color = params['color']
            params['color'] = COLOR_ALIASES.get(color, color)
        return super()._process_param_change(params)

    def _set_on_model(self, msg: Mapping[str, Any], root: Model, model: Model) -> None:
        if 'loading' in msg and isinstance(model, BkReactComponent):
            model.data.loading = msg.pop('loading')
        super()._set_on_model(msg, root, model)

    def _get_properties(self, doc: Document | None) -> dict[str, Any]:
        props = super()._get_properties(doc)
        props.pop('loading', None)
        props['data'].loading = self.loading
        return props

    @property
    def _synced_params(self) -> list[str]:
        ignored = ['default_layout']
        return [p for p in self.param if p not in ignored]

    def _update_loading(self, *_) -> None:
        pass

    def controls(self, parameters: list[str] = None, jslink: bool = True, **kwargs) -> Viewable:
        """
        Creates a set of widgets which allow manipulating the parameters
        on this instance. By default all parameters which support
        linking are exposed, but an explicit list of parameters can
        be provided.

        Parameters
        ----------
        parameters: list(str) | None
           An explicit list of parameters to return controls for.
        jslink: bool
           Whether to use jslinks instead of Python based links.
           This does not allow using all types of parameters.
        kwargs: dict
           Additional kwargs to pass to the Param pane(s) used to
           generate the controls widgets.

        Returns
        -------
        A layout of the controls
        """
        from .layout import Paper, Tabs
        from .widgets import LiteralInput

        parameters = parameters or []
        if parameters:
            linkable = parameters
        elif jslink:
            linkable = self._linkable_params
        else:
            linkable = list(self.param)

        if 'margin' not in kwargs:
            kwargs['margin'] = 0

        params = [p for p in linkable if p not in Viewable.param]
        controls = Param(self.param, parameters=params, default_layout=Paper,
                         name='Controls', **kwargs)
        layout_params = [p for p in linkable if p in Viewable.param]
        if 'name' not in layout_params and self._property_mapping.get('name', False) is not None and not parameters:
            layout_params.insert(0, 'name')
        style = Param(self.param, parameters=layout_params, default_layout=Paper,
                      name='Layout', **kwargs)
        if jslink:
            for p in params:
                widget = controls._widgets[p]
                widget.jslink(self, value=p, bidirectional=True)
                if isinstance(widget, LiteralInput):
                    widget.serializer = 'json'
            for p in layout_params:
                widget = style._widgets[p]
                widget.jslink(self, value=p, bidirectional=p != 'loading')
                if isinstance(widget, LiteralInput):
                    widget.serializer = 'json'

        if params and layout_params:
            return Tabs(controls.layout[0], style.layout[0])
        elif params:
            return controls.layout[0]
