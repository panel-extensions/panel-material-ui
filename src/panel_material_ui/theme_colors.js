// Dependency free so the contrast computation can be unit tested with node.

export const MIN_TEXT_CONTRAST = 4.5
// A primary that fails on a dark background is lightened by at least this
// much, so the tint stays clearly readable on elevated (lighter) surfaces.
export const MIN_TEXT_TINT = 0.35

export function parse_color(color) {
  if (typeof color !== "string") {
    return null
  }
  const value = color.trim().toLowerCase()
  let match = value.match(/^#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$/)
  if (match) {
    let hex = match[1]
    if (hex.length <= 4) {
      hex = hex.split("").map(c => c + c).join("")
    }
    return [0, 2, 4].map(i => parseInt(hex.slice(i, i + 2), 16))
  }
  match = value.match(/^rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)/)
  if (match) {
    return match.slice(1, 4).map(Number)
  }
  return null
}

function to_hex(rgb) {
  return `#${rgb.map(c => Math.round(c).toString(16).padStart(2, "0")).join("")}`
}

export function relative_luminance(rgb) {
  const [r, g, b] = rgb.map(c => {
    const v = c / 255
    return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

export function contrast_ratio(fg, bg) {
  const l1 = relative_luminance(fg)
  const l2 = relative_luminance(bg)
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)
}

// Mixes the color towards white, like MUI's lighten for an RGB color.
export function lighten_rgb(rgb, amount) {
  return rgb.map(c => c + (255 - c) * amount)
}

// Returns a text color derived from a primary color that reaches
// min_contrast against every background. A primary that already passes is
// returned unchanged; otherwise it is lightened by the smallest amount, but
// at least min_tint, that passes. Colors that cannot be parsed (e.g. CSS
// variables), or a light background no lighter tint passes on, return the primary.
export function primary_text_color(main, backgrounds, min_contrast = MIN_TEXT_CONTRAST, min_tint = MIN_TEXT_TINT) {
  const rgb = parse_color(main)
  const bgs = backgrounds.map(parse_color).filter(bg => bg != null)
  if (rgb == null || bgs.length === 0) {
    return main
  }
  const contrast = (color) => Math.min(...bgs.map(bg => contrast_ratio(color, bg)))
  if (contrast(rgb) >= min_contrast) {
    return main
  }
  for (let step = Math.round(min_tint * 100); step <= 100; step++) {
    const tint = lighten_rgb(rgb, step / 100)
    if (contrast(tint) >= min_contrast) {
      return to_hex(tint)
    }
  }
  return main
}
