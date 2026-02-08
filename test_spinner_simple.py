#!/usr/bin/env python3
"""
Minimal reproducible example for testing spinner hiding behavior.

Usage:
    python test_spinner_simple.py

Then open http://localhost:5006 in your browser.
"""
import time
import panel as pn

# Import after pn.extension
pn.extension()

from panel_material_ui.template import Page
import panel_material_ui as pmui


def trigger_busy(event):
    """Simulate a 3-second long operation"""
    time.sleep(3)


# Create control widgets
trigger_btn = pmui.Button(
    name='🚀 Trigger 3-Second Busy State',
    on_click=trigger_busy,
    color='success',
    sizing_mode='stretch_width'
)

# Instructions markdown
instructions = pn.pane.Markdown("""
# ✨ Spinner Hide Test

## 🎯 What to Test:

### 1. **Check Idle State** (Current)
Look at the header area right now - there should be **NO visible progress bar or spinner**.
The indicator should be completely invisible.

### 2. **Toggle Theme**
Click the sun/moon icon in the top-right to switch themes.
The indicator should remain invisible in both themes when idle.

### 3. **Change Indicator Type**
Use the dropdown below to switch between Linear (horizontal bar) and Circular (spinning circle).

### 4. **Trigger Busy State**
Click the green button below. After 1 second (debounce delay), you should see:
- **Linear**: A horizontal progress bar appear below the header toolbar
- **Circular**: A spinning circle appear in the top-right of the header

### 5. **Verify Hiding**
After 3 seconds, the indicator should smoothly fade out and become invisible again.

---

## ✅ Expected Behavior:

| State | What You Should See |
|-------|---------------------|
| **Idle** | Clean header, no visible indicator |
| **Busy** | Indicator smoothly fades in, animates |
| **After Busy** | Indicator smoothly fades out, becomes invisible |

---
""", sizing_mode='stretch_width')

# Spinner variant selector
spinner_select = pmui.Select(
    name='Busy Indicator Type',
    options=['linear', 'circular'],
    value='linear',
    width=300
)

# Status indicator
status = pn.pane.Markdown("""
### 📊 Current Status: **IDLE**

The busy indicator should be **invisible** right now.
""", sizing_mode='stretch_width')

# Create the page
page = Page(
    title='Spinner Hide Test',
    busy_indicator='linear',
    theme_toggle=True,  # Show theme toggle button
    main=[
        instructions,
        pn.pane.Markdown("## 🎮 Controls", sizing_mode='stretch_width'),
        spinner_select,
        trigger_btn,
        pn.pane.Markdown("---"),
        status,
    ],
    sidebar=[
        pn.pane.Markdown("## 📝 Test Checklist"),
        pn.pane.Markdown("""
        - [ ] Idle: Indicator invisible ✓
        - [ ] Dark theme: Works correctly
        - [ ] Light theme: Works correctly  
        - [ ] Linear: Hides when idle
        - [ ] Linear: Shows when busy
        - [ ] Circular: Hides when idle
        - [ ] Circular: Shows when busy
        - [ ] Smooth fade transitions
        """),
        pn.pane.Markdown("---"),
        pn.pane.Markdown("## 💡 Tips"),
        pn.pane.Markdown("""
        **Look at the header:**
        - Linear: Horizontal bar below toolbar
        - Circular: Circle in top-right corner
        
        **Timing:**
        - 1 sec: Debounce delay
        - 3 sec: Operation duration
        - Smooth: Fade transitions
        """)
    ]
)

# Wire up spinner variant selector
def update_spinner(event):
    page.busy_indicator = event.new
    status.object = f"""
### 📊 Current Status: **IDLE**

Indicator type: **{event.new.upper()}**

The busy indicator should be **invisible** right now.
"""

spinner_select.param.watch(update_spinner, 'value')

# Make page servable
page.servable()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Spinner Hide Test Server")
    print("=" * 60)
    print("\n📝 Instructions:")
    print("   1. Open http://localhost:5006 in your browser")
    print("   2. Follow the on-screen instructions")
    print("   3. Test both linear and circular indicators")
    print("   4. Test both light and dark themes")
    print("\n✨ Expected: Indicators are invisible when idle")
    print("=" * 60)
    
    pn.serve(page, port=5006, show=True)
