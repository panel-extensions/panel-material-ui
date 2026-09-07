import pytest

from panel_material_ui._utils import render_icon_tokens_html
from panel_material_ui.chat import ChatStep


@pytest.mark.parametrize("value", [None, "", 0, 1.5, ["a"]])
def test_render_icon_tokens_html_passthrough(value):
    assert render_icon_tokens_html(value) == value


def test_render_icon_tokens_html_plain_text_unchanged():
    assert render_icon_tokens_html("Plain title") == "Plain title"


def test_render_icon_tokens_html_single_token():
    result = render_icon_tokens_html(":material/bolt: Thinking")
    assert result.endswith(" Thinking")
    assert 'class="material-icons"' in result
    assert ">bolt</span>" in result


def test_render_icon_tokens_html_multiple_tokens():
    result = render_icon_tokens_html(":material/add:Both:material/remove:")
    assert result.count("<span") == 2
    assert ">add</span>" in result
    assert ">remove</span>" in result
    assert "Both" in result


def test_render_icon_tokens_html_variant_option():
    result = render_icon_tokens_html(":material/search@variant=outlined:")
    assert 'class="material-icons-outlined"' in result


def test_render_icon_tokens_html_variant_suffix():
    result = render_icon_tokens_html(":material/search_rounded:")
    assert 'class="material-icons-round"' in result
    assert ">search</span>" in result


def test_render_icon_tokens_html_color_and_size_options():
    result = render_icon_tokens_html(":material/search@color=red,icon_size=2rem:")
    assert "color: red" in result
    assert "font-size: 2rem" in result


def test_render_icon_tokens_html_unknown_option_ignored():
    result = render_icon_tokens_html(":material/search@nonsense=1:")
    assert 'class="material-icons"' in result
    assert "nonsense" not in result


@pytest.mark.parametrize("text", [
    ":material/:",
    ":material/not an icon:",
    ":material/search",
    "material/search:",
])
def test_render_icon_tokens_html_malformed_unchanged(text):
    assert render_icon_tokens_html(text) == text


def test_chat_step_title_renders_icon_span():
    step = ChatStep(title=":material/bolt: Thinking")
    assert 'class="material-icons"' in step._title_pane.object
    assert "Thinking" in step._title_pane.object


def test_chat_step_title_update_rerenders_icon_span():
    step = ChatStep(title="Plain")
    assert step._title_pane.object == "Plain"
    step.title = ":material/check: Done"
    assert ">check</span>" in step._title_pane.object
