from panel.config import config as _config

from .base import (
    BreakpointSwitcher,  # noqa
    Page,
    ThemeToggle,  # noqa
)

_config.param.template.objects['mui'] = Page
