"""
Automated Playwright test for spinner hiding behavior with screenshots and video.

This test will:
1. Test both light and dark themes
2. Test both linear and circular indicators
3. Capture screenshots of idle and busy states
4. Generate a video recording of the test
"""
import pytest
import time

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component
from playwright.sync_api import expect, Page as PlaywrightPage

from panel_material_ui.template import Page
from panel_material_ui import Button

pytestmark = pytest.mark.ui


def test_spinner_hiding_demo_with_screenshots(page: PlaywrightPage):
    """
    Comprehensive test with screenshots showing spinner hiding behavior.
    """
    # Start video recording
    context = page.context
    
    def slow_operation(event):
        time.sleep(3)
    
    trigger_btn = Button(name='Trigger Busy', on_click=slow_operation, color='success')
    theme_toggle = Button(name='Toggle Theme', color='primary')
    
    # Test with LinearProgress first
    pg = Page(
        title='Spinner Test',
        busy_indicator='linear',
        main=[
            pn.pane.Markdown("# Test LinearProgress Hiding"),
            trigger_btn,
            theme_toggle,
        ]
    )
    
    # Wire up theme toggle
    def toggle_theme(event):
        pg.dark_theme = not pg.dark_theme
    theme_toggle.on_click(toggle_theme)
    
    serve_component(page, pg)
    
    # Wait for page to fully load
    page.wait_for_timeout(1000)
    
    # Test 1: Linear Progress - Dark Theme - Idle State
    progress = page.locator(".MuiLinearProgress-root")
    expect(progress).to_be_attached()
    expect(progress).to_have_css("opacity", "0")
    page.screenshot(path="/tmp/1_linear_dark_idle.png", full_page=True)
    print("Screenshot 1: LinearProgress - Dark Theme - Idle (opacity: 0)")
    
    # Test 2: Linear Progress - Dark Theme - Busy State
    page.locator('button:has-text("Trigger Busy")').click()
    page.wait_for_timeout(1200)  # Wait for debounce + fade in
    expect(progress).to_have_css("opacity", "1")
    page.screenshot(path="/tmp/2_linear_dark_busy.png", full_page=True)
    print("Screenshot 2: LinearProgress - Dark Theme - Busy (opacity: 1)")
    
    # Wait for operation to complete
    page.wait_for_timeout(2500)
    
    # Test 3: Linear Progress - Dark Theme - Back to Idle
    expect(progress).to_have_css("opacity", "0")
    page.screenshot(path="/tmp/3_linear_dark_idle_after.png", full_page=True)
    print("Screenshot 3: LinearProgress - Dark Theme - Idle after busy (opacity: 0)")
    
    # Test 4: Linear Progress - Light Theme - Idle State
    page.locator('button:has-text("Toggle Theme")').click()
    page.wait_for_timeout(500)
    expect(progress).to_have_css("opacity", "0")
    page.screenshot(path="/tmp/4_linear_light_idle.png", full_page=True)
    print("Screenshot 4: LinearProgress - Light Theme - Idle (opacity: 0)")
    
    # Test 5: Linear Progress - Light Theme - Busy State
    page.locator('button:has-text("Trigger Busy")').click()
    page.wait_for_timeout(1200)
    expect(progress).to_have_css("opacity", "1")
    page.screenshot(path="/tmp/5_linear_light_busy.png", full_page=True)
    print("Screenshot 5: LinearProgress - Light Theme - Busy (opacity: 1)")
    
    # Wait for completion
    page.wait_for_timeout(2500)
    expect(progress).to_have_css("opacity", "0")
    
    # Now test CircularProgress
    pg.busy_indicator = 'circular'
    page.wait_for_timeout(500)
    
    # Test 6: Circular Progress - Light Theme - Idle State
    spinner = page.locator(".MuiCircularProgress-root")
    expect(spinner).to_be_attached()
    expect(spinner).to_have_css("opacity", "0")
    page.screenshot(path="/tmp/6_circular_light_idle.png", full_page=True)
    print("Screenshot 6: CircularProgress - Light Theme - Idle (opacity: 0)")
    
    # Test 7: Circular Progress - Light Theme - Busy State
    page.locator('button:has-text("Trigger Busy")').click()
    page.wait_for_timeout(1200)
    expect(spinner).to_have_css("opacity", "1")
    page.screenshot(path="/tmp/7_circular_light_busy.png", full_page=True)
    print("Screenshot 7: CircularProgress - Light Theme - Busy (opacity: 1)")
    
    # Wait for completion
    page.wait_for_timeout(2500)
    expect(spinner).to_have_css("opacity", "0")
    
    # Test 8: Circular Progress - Dark Theme - Idle State
    page.locator('button:has-text("Toggle Theme")').click()
    page.wait_for_timeout(500)
    expect(spinner).to_have_css("opacity", "0")
    page.screenshot(path="/tmp/8_circular_dark_idle.png", full_page=True)
    print("Screenshot 8: CircularProgress - Dark Theme - Idle (opacity: 0)")
    
    # Test 9: Circular Progress - Dark Theme - Busy State
    page.locator('button:has-text("Trigger Busy")').click()
    page.wait_for_timeout(1200)
    expect(spinner).to_have_css("opacity", "1")
    page.screenshot(path="/tmp/9_circular_dark_busy.png", full_page=True)
    print("Screenshot 9: CircularProgress - Dark Theme - Busy (opacity: 1)")
    
    page.wait_for_timeout(2500)
    expect(spinner).to_have_css("opacity", "0")
    
    print("\nAll tests passed! Screenshots saved to /tmp/")
    print("Summary:")
    print("- LinearProgress: Hidden when idle (opacity: 0), visible when busy (opacity: 1)")
    print("- CircularProgress: Hidden when idle (opacity: 0), visible when busy (opacity: 1)")
    print("- Works correctly in both light and dark themes")


if __name__ == "__main__":
    # Instructions for running this test
    print("To run this test with video recording:")
    print("pytest test_spinner_screenshots.py --headed --video on -v")
