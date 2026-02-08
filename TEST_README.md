# Spinner Hide Behavior - Test Applications

This directory contains test applications to manually and automatically verify that the LinearProgress and CircularProgress indicators properly hide when idle.

## Test Files

### 1. `test_spinner_simple.py` ⭐ **Recommended for Manual Testing**

The simplest standalone demo with clear on-screen instructions.

**Usage:**
```bash
python test_spinner_simple.py
```

Then open http://localhost:5006 in your browser.

**Features:**
- Clear visual instructions
- Theme toggle button (sun/moon icon in header)
- Indicator type selector (linear/circular)
- Button to trigger 3-second busy state
- Test checklist in sidebar

**What to verify:**
1. ✅ Indicator is invisible when idle (both themes)
2. ✅ Indicator appears after 1 second when button clicked
3. ✅ Indicator is visible and animating while busy
4. ✅ Indicator fades out and becomes invisible after completion
5. ✅ Works correctly in both light and dark themes
6. ✅ Works correctly for both linear and circular variants

---

### 2. `test_spinner_demo.py`

Full-featured demo with all controls.

**Usage:**
```bash
panel serve test_spinner_demo.py --show
```

**Features:**
- Theme toggle button
- Spinner variant selector
- Trigger button
- Detailed instructions and test checklist

---

### 3. `test_spinner_screenshots.py`

Automated Playwright test that captures screenshots of all states.

**Usage:**
```bash
pytest test_spinner_screenshots.py -v
```

**Features:**
- Tests both LinearProgress and CircularProgress
- Tests both light and dark themes
- Tests both idle and busy states
- Captures 9 screenshots to /tmp/:
  1. LinearProgress - Dark Theme - Idle
  2. LinearProgress - Dark Theme - Busy
  3. LinearProgress - Dark Theme - Idle (after busy)
  4. LinearProgress - Light Theme - Idle
  5. LinearProgress - Light Theme - Busy
  6. CircularProgress - Light Theme - Idle
  7. CircularProgress - Light Theme - Busy
  8. CircularProgress - Dark Theme - Idle
  9. CircularProgress - Dark Theme - Busy

---

## What Was Fixed

### Issue
The busy indicators (LinearProgress bar and CircularProgress spinner) were always visible in the Page header, even when idle. This created:
- Visual clutter in the header
- Poor color contrast, especially in light theme
- Confusing UX (looked like something was always loading)

### Solution
Applied CSS opacity transitions to both indicators:

```jsx
sx={{
  opacity: idle ? 0 : 1,  // Hidden when idle, visible when busy
  transition: theme.transitions.create("opacity", {
    duration: theme.transitions.duration.short,
  })
}}
```

### Benefits
1. **Clean UI**: Indicators only visible when actually busy
2. **Smooth transitions**: Professional fade in/out
3. **Theme compatible**: Works in both light and dark themes
4. **No layout shifts**: Elements stay in DOM, only visibility changes
5. **Debounced**: 1-second delay prevents flashing on quick operations

---

## Expected Behavior

### Idle State (Default)
- **LinearProgress**: Completely invisible (no horizontal bar)
- **CircularProgress**: Completely invisible (no spinner circle)
- Header looks clean and uncluttered

### Busy State (After clicking trigger button)
1. **First 1 second**: No visible change (debounce delay)
2. **After 1 second**: Indicator smoothly fades in (opacity: 0 → 1)
3. **During operation**: Indicator animates (progress bar moves, spinner spins)
4. **After 3 seconds**: Operation completes
5. **Immediately**: Indicator smoothly fades out (opacity: 1 → 0)

### Visual Comparison

**Before Fix:**
```
[Header with visible progress bar even when idle] ← Always visible! ❌
```

**After Fix:**
```
[Clean header, no visible indicators]              ← Hidden when idle ✅
      ↓ (user clicks button)
[Smooth fade in after 1 sec]
      ↓ (3 seconds pass)
[Smooth fade out]
      ↓
[Clean header again]                               ← Hidden when idle ✅
```

---

## Testing Checklist

Use this checklist when manually testing:

### LinearProgress (Horizontal Bar)
- [ ] Invisible when page loads (dark theme)
- [ ] Invisible when page loads (light theme)
- [ ] Appears smoothly when busy triggered
- [ ] Animates during busy state
- [ ] Disappears smoothly when busy completes
- [ ] Returns to invisible state

### CircularProgress (Spinning Circle)
- [ ] Invisible when page loads (dark theme)
- [ ] Invisible when page loads (light theme)
- [ ] Appears smoothly when busy triggered
- [ ] Spins during busy state
- [ ] Disappears smoothly when busy completes
- [ ] Returns to invisible state

### Theme Compatibility
- [ ] Works correctly in dark theme
- [ ] Works correctly in light theme
- [ ] Smooth theme transitions

---

## Implementation Details

### Files Modified
- `src/panel_material_ui/template/Page.jsx`
  - Added `opacity: idle ? 0 : 1` to LinearProgress
  - Added `opacity: idle ? 0 : 1` to CircularProgress
  - Changed colors to "inherit" for theme compatibility
  - Added smooth MUI transitions

- `tests/ui/template/test_page.py`
  - Added tests for LinearProgress hiding when idle
  - Added tests for LinearProgress showing when busy
  - Added tests for CircularProgress hiding when idle
  - Added tests for CircularProgress showing when busy

### Technical Approach
- Uses CSS `opacity` instead of display/visibility for smooth transitions
- Leverages MUI's built-in transition system for consistency
- Maintains DOM stability (no layout shifts)
- Works with existing 1-second debounce logic

---

## Troubleshooting

### Indicator still visible when idle
- Check browser DevTools
- Verify opacity is actually 0
- Check for CSS conflicts

### No smooth transitions
- Verify MUI theme is loaded
- Check browser supports CSS transitions
- Try hard refresh (Ctrl+Shift+R)

### Indicator doesn't appear when busy
- Check console for errors
- Verify busy state is actually triggered
- Check if debounce is working (wait >1 second)

---

## Quick Start

**Fastest way to test:**

```bash
# 1. Run the simple demo
python test_spinner_simple.py

# 2. Open browser to http://localhost:5006

# 3. Verify:
#    - Header looks clean (no visible bar/spinner)
#    - Click green button
#    - Bar/spinner appears after 1 second
#    - Bar/spinner disappears after 3 more seconds
#    - Try toggling theme (sun/moon icon)
#    - Try switching indicator type (dropdown)
```

That's it! 🎉
