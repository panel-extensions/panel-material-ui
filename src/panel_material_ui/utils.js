import * as React from "react"
import {grey} from "@mui/material/colors"
import {createTheme} from "@mui/material/styles"
import {deepmerge} from "@mui/utils"

export const int_regex = /^[-+]?\d*$/
export const float_regex = /^[-+]?\d*\.?\d*(?:(?:\d|\d.)[eE][-+]?)*\d*$/

export class SessionStore {
  constructor() {
    this.shared_var = null
    this._callbacks = []
  }

  set_value(value) {
    const old = this.shared_var
    this.shared_var = value
    if (value !== old) {
      for (const cb of this._callbacks) {
        cb(value)
      }
    }
  }

  get_value() {
    return this.shared_var
  }

  subscribe(callback) {
    this._callbacks.push(callback)
    return () => this._callbacks.splice(this._callbacks.indexOf(callback), 1)
  }

  unsubscribe(callback) {
    this._callbacks.splice(this._callbacks.indexOf(callback), 1)
  }
}

export const dark_mode = new SessionStore()

export function render_theme_css(theme) {
  const dark = theme.palette.mode === "dark"
  return `
    :root, :host {
      --panel-primary-color: ${theme.palette.primary.main};
      --panel-on-primary-color: ${theme.palette.primary.contrastText};
      --panel-secondary-color: ${theme.palette.secondary.main};
      --panel-on-secondary-color: ${theme.palette.secondary.contrastText};
      --panel-background-color: ${theme.palette.background.default};
      --panel-on-background-color: ${theme.palette.text.primary};
      --panel-surface-color: ${theme.palette.background.paper};
      --panel-on-surface-color: ${theme.palette.text.primary};
      --code-bg-color: #263238;
      --code-text-color: #82aaff;
      --success-bg-color: ${theme.palette.success.main};
      --success-text-color: ${theme.palette.success.contrastText};
      --danger-bg-color: ${theme.palette.error.main};
      --danger-text-color: ${theme.palette.error.contrastText};
      --info-bg-color: ${theme.palette.info.main};
      --info-text-color: ${theme.palette.info.contrastText};
      --primary-bg-color: #0d6efd;
      --secondary-bg-color: #6c757d;
      --warning-bg-color: #ffc107;
      --light-bg-color: #f8f9fa;
      --dark-bg-color: #212529;
      --primary-text-color: #0a58ca;
      --secondary-text-color: #6c757d;
      --warning-text-color: #997404;
      --light-text-color: #6c757d;
      --dark-text-color: #495057;
      --primary-bg-subtle: ${dark ? "#031633" : "#cfe2ff"};
      --secondary-bg-subtle: ${dark ? "#212529" : "#f8f9fa"};
      --success-bg-subtle: ${dark ? "#051b11" : "#d1e7dd"};
      --info-bg-subtle: ${dark ? "#032830" : "#cff4fc"};
      --warning-bg-subtle: ${dark ? "#332701" : "#fff3cd"};
      --danger-bg-subtle: ${dark ? "#2c0b0e" : "#f8d7da"};
      --light-bg-subtle: ${dark ? "#343a40" : "#fcfcfd"};
      --dark-bg-subtle: ${dark ? "#1a1d20" : "#ced4da"};
      --primary-border-subtle: ${dark ? "#084298" : "#9ec5fe"};
      --secondary-border-subtle: ${dark ? "#495057" : "#e9ecef"};
      --success-border-subtle: ${dark ? "#0f5132" : "#a3cfbb"};
      --info-border-subtle: ${dark ? "#055160" : "#9eeaf9"};
      --warning-border-subtle: ${dark ? "#664d03" : "#ffe69c"};
      --danger-border-subtle: ${dark ? "#842029" : "#f1aeb5"};
      --light-border-subtle: ${dark ? "#495057" : "#e9ecef"};
      --dark-border-subtle: ${dark ? "#343a40" : "#adb5bd"};
      --bokeh-font-size: ${theme.typography.fontSize}px;
      --bokeh-base-font: ${theme.typography.fontFamily};
    }
  `
}

function find_on_parent(view, prop) {
  let current = view
  const elevations = []
  while (current != null) {
    if (current.model?.data?.[prop] != null) {
      return current.model.data[prop]
    }
    current = current.parent
  }
  return null
}

function hexToRgb(hex, asString=false) {
  hex = hex.replace(/^#/, "");
  if (hex.length === 3) {
    hex = hex.split("").map(c => c + c).join("");
  }
  const bigint = parseInt(hex, 16);
  const rgb = {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255
  }
  return asString ? `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})` : rgb
}

function compositeColors(fg, bg, alpha) {
  return {
    r: Math.round((1 - alpha) * bg.r + alpha * fg.r),
    g: Math.round((1 - alpha) * bg.g + alpha * fg.g),
    b: Math.round((1 - alpha) * bg.b + alpha * fg.b),
  };
}

function rgbToHsl(r, g, b) {
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s;
  const l = (max + min) / 2;

  if (max === min) {
    h = s = 0; // achromatic
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    h /= 6;
  }

  return [h, s, l];
}

function hslToRgb(h, s, l) {
  if (s === 0) { return [l, l, l]; } // achromatic

  const hue2rgb = (p, q, t) => {
    if (t < 0) { t += 1; }
    if (t > 1) { t -= 1; }
    if (t < 1 / 6) { return p + (q - p) * 6 * t; }
    if (t < 1 / 2) { return q; }
    if (t < 2 / 3) { return p + (q - p) * (2 / 3 - t) * 6; }
    return p;
  };

  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;

  return [
    hue2rgb(p, q, h + 1 / 3),
    hue2rgb(p, q, h),
    hue2rgb(p, q, h - 1 / 3),
  ];
}

function generatePalette(color, nColors = 3) {
  // Remove the leading "#" if present
  const hex = color.replace(/^#/, "");

  // Convert hex to normalized RGB
  const r = parseInt(hex.slice(0, 2), 16) / 255;
  const g = parseInt(hex.slice(2, 4), 16) / 255;
  const b = parseInt(hex.slice(4, 6), 16) / 255;

  // Convert RGB to HSL
  const [hBase, s, l] = rgbToHsl(r, g, b);

  // Generate evenly spaced hues
  const hues = Array.from({length: nColors}, (_, i) => (hBase + i / nColors) % 1);

  // Convert back to hex colors
  return hues.map(h => {
    const [rOut, gOut, bOut] = hslToRgb(h, s, l);
    return (
      `#${
        [rOut, gOut, bOut]
          .map(v => Math.round(v * 255).toString(16).padStart(2, "0"))
          .join("")}`
    );
  });
}

const overlayOpacities = [
  0,
  0.051,
  0.069,
  0.082,
  0.092,
  0.101,
  0.108,
  0.114,
  0.119,
  0.124,
  0.128,
  0.132,
  0.135,
  0.139,
  0.142,
  0.145,
  0.147,
  0.150,
  0.152,
  0.155,
  0.157,
  0.159,
  0.161,
  0.163,
  0.165,
];

function getOverlayOpacity(elevation) {
  if (elevation < 1) { return 0; }
  if (elevation >= 24) { return overlayOpacities[24]; }
  return overlayOpacities[Math.floor(elevation)];
}

function getMuiElevatedColor(backgroundHex, elevation, isDarkMode = false) {
  const bg = hexToRgb(backgroundHex);
  const opacity = getOverlayOpacity(elevation);
  const fg = isDarkMode ? {r: 255, g: 255, b: 255} : {r: 0, g: 0, b: 0};
  const result = compositeColors(fg, bg, opacity);
  return `rgb(${result.r}, ${result.g}, ${result.b})`;
}

function elevation_color(elevation, theme, dark) {
  return (dark && elevation) ? getMuiElevatedColor(theme.palette.background.paper, elevation, dark) : theme.palette.background.paper
}

function apply_plotly_theme(model, theme, dark, font_family) {
  const view = Bokeh.index.find_one_by_id(model.id)
  const elevation = view ? find_on_parent(view, "elevation") : 0
  let paper_color = elevation_color(elevation, theme, dark)
  paper_color = paper_color.startsWith("#") ? hexToRgb(paper_color, true) : paper_color
  const paper_bgcolor = paper_color
  const plot_bgcolor = paper_color
  const font_color_primary = theme.palette.text.primary
  const font_color_secondary = theme.palette.text.secondary
  const grid_color = theme.palette.divider
  const axis_line_color = theme.palette.divider
  const zero_line_color = theme.palette.divider
  if (model.layout.colorway == null && !model.tags.includes("auto-palette")) {
    model.tags.push("auto-palette")
  }
  const colorway = model.tags.includes("auto-palette") ? generatePalette(theme.palette.primary.main, 10) : model.layout.colorway

  const layout = {
    colorway,
    font: {
      color: font_color_primary,
      family: font_family,
      size: 12,
    },
    paper_bgcolor,
    plot_bgcolor,
    margin: {l: 64, r: 64, t: 64, b: 64},
    title: {
      font: {size: 16, color: font_color_primary},
      x: 0.5,
      xanchor: "center",
      pad: {t: 20},
    },
    xaxis: {
      gridcolor: grid_color,
      linecolor: axis_line_color,
      zerolinecolor: zero_line_color,
      tickcolor: axis_line_color,
      tickfont: {color: font_color_secondary, size: 11},
      title: {
        font: {size: 14, color: font_color_primary},
        standoff: 20,
      },
      showline: true,
      linewidth: 1,
      gridwidth: 1,
      zerolinewidth: 1,
    },
    yaxis: {
      gridcolor: grid_color,
      linecolor: axis_line_color,
      zerolinecolor: zero_line_color,
      tickcolor: axis_line_color,
      tickfont: {color: font_color_secondary, size: 11},
      title: {
        font: {size: 14, color: font_color_primary},
        standoff: 20,
      },
      showline: true,
      linewidth: 1,
      gridwidth: 1,
      zerolinewidth: 1,
    },
    coloraxis: {
      colorbar: {
        outlinewidth: 0,
        ticks: "",
        tickcolor: axis_line_color,
        tickfont: {color: font_color_secondary},
        title: {font: {color: font_color_primary}},
      }
    },

    legend: {
      bgcolor: "rgba(255, 255, 255, 0)",
      bordercolor: "rgba(0, 0, 0, 0)",
      font: {color: font_color_primary},
      orientation: "v",
      x: 1.02,
      xanchor: "left",
    },

    hoverlabel: {
      bgcolor: paper_bgcolor,
      bordercolor: grid_color,
      font: {color: font_color_primary},
    },
    annotationdefaults: {
      arrowcolor: font_color_primary,
      arrowhead: 0,
      arrowwidth: 1,
      font: {color: font_color_primary},
    },
    geo: {
      bgcolor: paper_bgcolor,
      lakecolor: paper_bgcolor,
      landcolor: paper_bgcolor,
    },

    polar: {
      bgcolor: paper_bgcolor,
      angularaxis: {
        gridcolor: grid_color,
        linecolor: axis_line_color,
      },
      radialaxis: {
        gridcolor: grid_color,
        linecolor: axis_line_color,
      },
    },
    ternary: {
      bgcolor: paper_bgcolor,
      aaxis: {
        gridcolor: grid_color,
        linecolor: axis_line_color,
      },
      baxis: {
        gridcolor: grid_color,
        linecolor: axis_line_color,
      },
      caxis: {
        gridcolor: grid_color,
        linecolor: axis_line_color,
      },
    },
  }

  const data = {
    bar: [
      {
        marker: {
          line: {color: paper_bgcolor, width: 0.5},
          opacity: 0.8,
        },
        textfont: {color: font_color_primary},
      }
    ],
    scatter: [
      {
        marker: {
          size: 8,
          line: {color: paper_bgcolor, width: 0.5},
          opacity: 0.8,
        },
        textfont: {color: font_color_primary},
      }
    ],
    scatter3d: [
      {
        marker: {
          size: 4,
          line: {color: paper_bgcolor, width: 0.5},
          opacity: 0.8,
        }
      }
    ],
    histogram: [
      {
        marker: {
          line: {color: paper_bgcolor, width: 0.5},
          opacity: 0.7,
        }
      }
    ],
    box: [
      {
        boxpoints: "outliers",
        fillcolor: "rgba(255,255,255,0)",
        line: {color: font_color_primary},
        marker: {opacity: 0.8, size: 3},
      }
    ],
    violin: [
      {
        fillcolor: "rgba(255,255,255,0)",
        line: {color: font_color_primary},
        marker: {opacity: 0.8, size: 3},
      }
    ],
    heatmap: [
      {
        colorbar: {
          outlinewidth: 0,
          ticks: "",
          tickcolor: axis_line_color,
          tickfont: {color: font_color_secondary},
          title: {font: {color: font_color_primary}},
        },
        colorscale: [
          [0, colorway ? colorway[1] : "#f44336"],     // Red
          [0.25, dark ? "#424242" : "#ffffff"],        // White/Gray
          [0.5, dark ? "#616161" : "#e0e0e0"],         // Light Gray
          [0.75, colorway ? colorway[0] : "#1976d2"],  // Primary blue
          [1, colorway ? colorway[2] : "#0d47a1"]      // Dark blue
        ],
      }
    ],
    contour: [
      {
        colorbar: {
          outlinewidth: 0,
          ticks: "",
          tickcolor: axis_line_color,
          tickfont: {color: font_color_secondary},
          title: {font: {color: font_color_primary}},
        },
        colorscale: [
          [0, colorway ? colorway[1] : "#f44336"],    // Red
          [0.33, colorway ? colorway[2] : "#4caf50"], // Green
          [0.67, colorway ? colorway[4] : "#ff9800"], // Orange
          [1, colorway ? colorway[1] : "#f44336"]     // Red
        ],
        line: {color: axis_line_color, width: 0.5},
      }
    ],
    surface: [
      {
        colorbar: {
          outlinewidth: 0,
          ticks: "",
          tickcolor: axis_line_color,
          tickfont: {color: font_color_secondary},
          title: {font: {color: font_color_primary}},
        },
        colorscale: [
          [0, colorway ? colorway[0] : "#1976d2"],           // Primary blue
          [0.25, colorway ? colorway[3] : "#2196f3"], // Light blue
          [0.5, colorway ? colorway[2] : "#4caf50"],  // Green
          [0.75, colorway ? colorway[4] : "#ff9800"], // Orange
          [1, colorway ? colorway[1] : "#f44336"]     // Red
        ],
      }
    ],
    candlestick: [
      {
        increasing: {
          line: {color: "#4caf50"},
          fillcolor: "#4caf50",
        },
        decreasing: {
          line: {color: "#f44336"},
          fillcolor: "#f44336",
        },
      }
    ],
    ohlc: [
      {
        increasing: {line: {color: "#4caf50"}},
        decreasing: {line: {color: "#f44336"}},
      }
    ],
    waterfall: [
      {
        decreasing: {marker: {color: colorway && colorway.length > 1 ? colorway[1] : "#f44336"}},
        increasing: {marker: {color: colorway ? colorway[0] : "#1976d2"}},
        totals: {marker: {color: "#9e9e9e"}},
        textfont: {color: font_color_primary},
        textposition: "outside",
        connector: {line: {color: axis_line_color, width: 1}},
      }
    ],
    funnel: [
      {
        textfont: {color: font_color_primary},
        textposition: "inside",
        connector: {line: {color: axis_line_color, width: 1}},
      }
    ],
    pie: [
      {
        textfont: {color: font_color_primary},
        textposition: "auto",
        marker: {line: {color: paper_bgcolor, width: 2}},
      }
    ],
    sunburst: [
      {
        textfont: {color: font_color_primary},
        marker: {line: {color: paper_bgcolor, width: 2}},
      }
    ],
    treemap: [
      {
        textfont: {color: font_color_primary},
        marker: {line: {color: paper_bgcolor, width: 2}},
      }
    ],
    icicle: [
      {
        textfont: {color: font_color_primary},
        marker: {line: {color: paper_bgcolor, width: 2}},
      }
    ],
    sankey: [
      {
        node: {
          color: colorway ? colorway[0] : "#1976d2",
          line: {color: axis_line_color, width: 0.5},
        },
        link: {color: "rgba(128, 128, 128, 0.4)"},
      }
    ],
    parcoords: [
      {
        line: {
          colorscale: [
            [0, colorway ? colorway[0] : "#1976d2"],
            [0.5, colorway ? colorway[2] : "#4caf50"],
            [1, colorway ? colorway[1] : "#f44336"]
          ],
          showscale: true
        },
        labelangle: 0,
        labelfont: {color: font_color_primary},
        tickfont: {color: font_color_secondary},
      }
    ],
    parcats: [
      {
        labelfont: {color: font_color_primary},
        tickfont: {color: font_color_secondary},
        line: {
          colorscale: [
            [0, colorway ? colorway[0] : "#1976d2"],
            [0.5, colorway ? colorway[2] : "#4caf50"],
            [1, colorway ? colorway[1] : "#f44336"]
          ]
        },
      }
    ],
    table: [
      {
        header: {
          fill: {color: grid_color},
          font: {color: font_color_primary, size: 12},
          line: {color: axis_line_color, width: 1},
        },
        cells: {
          fill: {color: paper_bgcolor},
          font: {color: font_color_primary, size: 11},
          line: {color: axis_line_color, width: 1},
        },
      }
    ],
    mesh3d: [
      {
        colorbar: {
          outlinewidth: 0,
          ticks: "",
          tickcolor: axis_line_color,
          tickfont: {color: font_color_secondary},
          title: {font: {color: font_color_primary}},
        },
        colorscale: [
          [0, colorway ? colorway[0] : "#1976d2"],
          [0.33, colorway ? colorway[2] : "#4caf50"],
          [0.67, colorway ? colorway[4] : "#ff9800"],
          [1, colorway ? colorway[1] : "#f44336"]
        ],
      }
    ],
    isosurface: [
      {
        colorbar: {
          outlinewidth: 0,
          ticks: "",
          tickcolor: axis_line_color,
          tickfont: {color: font_color_secondary},
          title: {font: {color: font_color_primary}},
        },
        colorscale: [
          [0, colorway ? colorway[0] : "#1976d2"],
          [0.33, colorway ? colorway[2] : "#4caf50"],
          [0.67, colorway ? colorway[4] : "#ff9800"],
          [1, colorway ? colorway[1] : "#f44336"]
        ],
      }
    ],

    volume: [
      {
        colorbar: {
          outlinewidth: 0,
          ticks: "",
          tickcolor: axis_line_color,
          tickfont: {color: font_color_secondary},
          title: {font: {color: font_color_primary}},
        },
        colorscale: [
          [0, colorway ? colorway[0] : "#1976d2"],
          [0.33, colorway ? colorway[2] : "#4caf50"],
          [0.67, colorway ? colorway[4] : "#ff9800"],
          [1, colorway ? colorway[1] : "#f44336"]
        ],
      }
    ],
  }

  model.setv({
    layout: deepmerge(model.layout, layout),
    data: model.data.map((d) => data[d.type] ? deepmerge(d, data[d.type]) : d),
  })
}

function apply_bokeh_theme(model, theme, dark, font_family) {
  const model_props = {}
  const model_type = model.type
  if (model_type.endsWith("Axis")) {
    model_props.axis_label_text_color = theme.palette.text.primary
    model_props.axis_label_text_font = font_family
    model_props.axis_line_alpha = dark ? 0 : 1
    model_props.axis_line_color = theme.palette.text.primary
    model_props.major_label_text_color = theme.palette.text.primary
    model_props.major_label_text_font = font_family
    model_props.major_tick_line_alpha = dark ? 0 : 1
    model_props.major_tick_line_color = theme.palette.text.primary
    model_props.minor_tick_line_alpha = dark ? 0 : 1
    model_props.minor_tick_line_color = theme.palette.text.primary
  } else if (model_type.endsWith("Legend")) {
    const view = Bokeh.index.find_one_by_id(model.id)
    const elevation = view ? find_on_parent(view, "elevation") : 0
    model_props.background_fill_color = elevation_color(elevation, theme, dark)
    model_props.border_line_alpha = dark ? 0 : 1
    model_props.title_text_color = theme.palette.text.primary
    model_props.title_text_font = font_family
    model_props.label_text_color = theme.palette.text.primary
    model_props.label_text_font = font_family
  } else if (model_type.endsWith("ColorBar")) {
    const view = Bokeh.index.find_one_by_id(model.id)
    const elevation = view ? find_on_parent(view, "elevation") : 0
    model_props.background_fill_color = elevation_color(elevation, theme, dark)
    model_props.title_text_color = theme.palette.text.primary
    model_props.title_text_font = font_family
    model_props.major_label_text_color = theme.palette.text.primary
    model_props.major_label_text_font = font_family
  } else if (model_type.endsWith("Title")) {
    model_props.text_color = theme.palette.text.primary
    model_props.text_font = font_family
  } else if (model_type.endsWith("Grid")) {
    if (model_props.grid_line_color != null) {
      model_props.grid_line_color = theme.palette.text.primary
      model_props.grid_line_alpha = dark ? 0.25 : 0.5
    }
  } else if (model_type.endsWith("Canvas")) {
    model_props.stylesheets = [...model.stylesheets, ":host { --highlight-color: none }"]
  } else if (model_type.endsWith("Figure")) {
    const view = Bokeh.index.find_one_by_id(model.id)
    const elevation = view ? find_on_parent(view, "elevation") : 0
    model_props.background_fill_color = theme.palette.background.paper
    model_props.border_fill_color = elevation_color(elevation, theme, dark)
    model_props.outline_line_color = theme.palette.text.primary
    model_props.outline_line_alpha = dark ? 0.25 : 0
    if (view) {
      apply_bokeh_theme(view.canvas_view.model, theme, dark, font_family)
    }
  } else if (model_type.endsWith("Toolbar")) {
    const stylesheet = `.bk-right.bk-active, .bk-above.bk-active {
--highlight-color: ${theme.palette.primary.main} !important;
    }`
    model_props.stylesheets = [...model.stylesheets, stylesheet]
  } else if (model_type.endsWith("Tooltip")) {
    model.stylesheets = [...model.stylesheets, `
      .bk-tooltip-row-label {
        color: ${theme.palette.primary.main} !important;
      `
    ]
  } else if (model_type.endsWith("AcePlot")) {
    model_props.theme = dark ? "github_dark" : "github_light_default"
  } else if (model_type.endsWith("VegaPlot")) {
    model_props.theme = dark ? "dark" : null
  } else if (model_type.endsWith("PlotlyPlot")) {
    apply_plotly_theme(model, theme, dark, font_family)
  } else if (model_type.endsWith("HoverTool")) {
    const view = Bokeh.index.find_one_by_id(model.id)
    if (view) {
      view.ttmodels.forEach(ttmodel => {
        apply_bokeh_theme(ttmodel, theme, dark, font_family)
      })
    }
  }
  if (Object.keys(model_props).length > 0) {
    model.setv(model_props)
  }
}

export function render_theme_config(props, theme_config, dark_theme) {
  const config = {
    cssVariables: {
      rootSelector: ":host",
      colorSchemeSelector: "class",
    },
    palette: {
      mode: dark_theme ? "dark" : "light",
      default: {
        main: dark_theme ? grey[500] : "#000000",
        light: grey[dark_theme ? 200 : 100],
        dark: grey[dark_theme ? 800 : 600],
        contrastText: dark_theme ? "#ffffff" : "#ffffff",
      },
      dark: {
        main: grey[dark_theme ? 800 : 600],
        light: grey[dark_theme ? 700 : 400],
        dark: grey[dark_theme ? 900 : 800],
        contrastText: "#ffffff",
      },
      light: {
        main: grey[200],
        light: grey[100],
        dark: grey[300],
        contrastText: "#000000",
      },
    },
    components: {
      MuiPopover: {
        defaultProps: {
          container: props.view.container,
        },
      },
      MuiPopper: {
        defaultProps: {
          container: props.view.container,
        },
      },
      MuiModal: {
        defaultProps: {
          container: props.view.container,
        },
      },
      MuiIconButton: {
        styleOverrides: {
          root: {
            variants: [
              {
                props: {color: "default"},
                style: {
                  color: "var(--mui-palette-default-dark)",
                },
              },
            ],
          },
        },
      },
      MuiSwitch: {
        styleOverrides: {
          switchBase: {
            "&.MuiSwitch-colorDefault.Mui-checked": {
              color: "var(--mui-palette-default-contrastText)",
            },
            "&.MuiSwitch-colorDefault.Mui-checked + .MuiSwitch-track": {
              backgroundColor: "var(--mui-palette-default-main)",
              opacity: 0.7,
            },
          },
        },
      },
      MuiSlider: {
        styleOverrides: {
          root: {
            "& .MuiSlider-thumbColorDefault": {
              backgroundColor: "var(--mui-palette-default-contrastText)",
            },
            variants: [
              {
                props: {color: "default"},
                style: {
                  color: "var(--mui-palette-default-dark)",
                },
              },
            ],
          },
        },
      },
      MuiToggleButton: {
        styleOverrides: {
          root: {
            "&.MuiToggleButton-default.Mui-selected": {
              backgroundColor: "var(--mui-palette-default-light)",
              color: "var(--mui-palette-default-dark)",
            },
          },
        },
      },
      MuiFab: {
        styleOverrides: {
          root: {
            "&.MuiFab-default": {
              color: "var(--mui-palette-default-main)",
              backgroundColor: "var(--mui-palette-default-contrastText)",
            },
          }
        },
      },
      MuiTab: {
        styleOverrides: {
          root: {
            "&.MuiTab-textColorDefault": {
              color: "var(--mui-palette-default-main)"
            }
          }
        }
      },
      MuiButton: {
        styleOverrides: {
          root: {
            variants: [
              {
                props: {variant: "contained", color: "default"},
                style: {
                  backgroundColor: `var(--mui-palette-default-${dark_theme ? "dark": "contrastText"})`,
                  color: `var(--mui-palette-default-${dark_theme ? "contrastText" : "main"})`,
                  "&:hover": {
                    backgroundColor: "var(--mui-palette-default-light)",
                    color: "var(--mui-palette-default-dark)",
                  },
                },
              },
              {
                props: {variant: "outlined", color: "default"},
                style: {
                  borderColor: "var(--mui-palette-default-main)",
                  color: "var(--mui-palette-default-main)",
                  "&:hover": {
                    backgroundColor: "var(--mui-palette-default-light)",
                    color: "var(--mui-palette-default-dark)"
                  },
                },
              },
              {
                props: {variant: "text", color: "default"},
                style: {
                  color: "var(--mui-palette-default-main)",
                  "&:hover": {
                    backgroundColor: "var(--mui-palette-default-light)",
                    color: "var(--mui-palette-default-dark)",
                  },
                },
              },
            ],
            textTransform: "none",
          },
        },
      },
      MuiMultiSectionDigitalClock: {
        styleOverrides: {
          root: {
            minWidth: "165px"
          }
        }
      }
    }
  }
  if (theme_config != null) {
    return deepmerge(config, theme_config)
  }
  return config
}

export const setup_global_styles = (theme) => {
  let global_style_el = document.querySelector("#global-styles-panel-mui")
  const template_style_el = document.querySelector("#template-styles")
  const theme_ref = React.useRef(theme)
  if (!global_style_el) {
    {
      global_style_el = document.createElement("style")
      global_style_el.id = "global-styles-panel-mui"
      if (template_style_el) {
        document.head.insertBefore(global_style_el, template_style_el)
      } else {
        document.head.appendChild(global_style_el)
      }
    }
  }
  let page_style_el = document.querySelector("#page-style")
  if (!page_style_el) {
    page_style_el = document.createElement("style")
    page_style_el.id = "page-style"
    if (template_style_el) {
      document.head.insertBefore(page_style_el, template_style_el)
    } else {
      document.head.appendChild(page_style_el)
    }
  }

  React.useEffect(() => {
    const doc = window.Bokeh.documents[window.Bokeh.documents.length-1]
    const cb = (e) => {
      if (e.kind !== "ModelChanged") {
        return
      }
      const value = e.value
      const models = []
      if (Array.isArray(value)) {
        value.forEach(v => {
          if (v && v.document === doc) {
            models.push(v)
          }
        })
      } else if (value && value.document === doc) {
        models.push(value)
      }
      if (models.length === 0) {
        return
      }
      const theme = theme_ref.current
      const dark = theme.palette.mode === "dark"
      const font_family = Array.isArray(theme.typography.fontFamily) ? (
        theme.typography.fontFamily.join(", ")
      ) : (
        theme.typography.fontFamily
      )
      models.forEach(model => {
        model.references().forEach((ref) => {
          apply_bokeh_theme(ref, theme, dark, font_family)
        })
        apply_bokeh_theme(model, theme, dark, font_family)
      })
    }
    doc.on_change(cb)
    return () => doc.remove_on_change(cb)
  }, [])

  React.useEffect(() => {
    theme_ref.current = theme
    const dark = theme.palette.mode === "dark"
    const doc = window.Bokeh.documents[window.Bokeh.documents.length-1]
    const font_family = Array.isArray(theme.typography.fontFamily) ? (
      theme.typography.fontFamily.join(", ")
    ) : (
      theme.typography.fontFamily
    )
    doc.all_models.forEach(model => apply_bokeh_theme(model, theme, dark, font_family))
    global_style_el.textContent = render_theme_css(theme)
    const style_objs = theme.generateStyleSheets()
    const css = style_objs
      .map((obj) => {
        return Object.entries(obj).map(([selector, vars]) => {
          const varLines = Object.entries(vars)
            .map(([key, val]) => `  ${key}: ${val};`)
            .join("\n");
          return `:root, ${selector} {\n${varLines}\n}`;
        })
          .join("\n\n");
      })
      .join("\n\n");
    page_style_el.textContent = css
  }, [theme])
}

export const install_theme_hooks = (props) => {
  const [dark_theme, setDarkTheme] = props.model.useState("dark_theme")

  // ALERT: Unclear why this is needed, the dark_theme state variable
  // on it's own does not seem stable
  const dark_ref = React.useRef(dark_theme)
  React.useEffect(() => {
    dark_ref.current = dark_theme
  }, [dark_theme])

  // Apply .mui-dark or .mui-light to the container
  const themeClass = `mui-${dark_theme ? "dark" : "light"}`
  const inverseClass = `mui-${dark_theme ? "light" : "dark"}`
  props.view.container.className = `${props.view.container.className.replace(inverseClass, "").replace(themeClass, "").trim()} ${themeClass}`.trim()

  const merge_theme_configs = (view) => {
    let current = view
    const theme_configs = []
    const views = []
    while (current != null) {
      if (current.model?.data?.theme_config !== undefined) {
        const config = current.model.data.theme_config
        views.push(current)
        if (config !== null) {
          theme_configs.push((config.dark && config.light) ? config[dark_ref.current ? "dark" : "light"] : config)
        }
      }
      current = current.parent
    }
    const merged = theme_configs.reverse().reduce((acc, config) => deepmerge(acc, config), {})
    return [merged, views]
  }

  const [theme_config, setThemeConfig] = React.useState(() => merge_theme_configs(props.view, dark_ref.current)[0])
  const update_views = () => setThemeConfig(merge_theme_configs(props.view)[0])

  React.useEffect(() => {
    const [_, views] = merge_theme_configs(props.view)
    const cb = () => update_views()
    for (const view of views) {
      view.model_proxy.on("theme_config", cb)
    }
    return () => {
      for (const view of views) {
        view.model_proxy.off("theme_config", cb)
      }
    }
  }, [])
  React.useEffect(() => update_views(), [dark_theme])
  const theme = React.useMemo(() => {
    const config = render_theme_config(props, theme_config, dark_theme)
    return createTheme(config)
  }, [dark_theme, theme_config])

  // Sync local dark_mode with global dark mode
  const isFirstRender = React.useRef(true)
  React.useEffect(() => {
    if (isFirstRender.current && dark_mode.get_value() != null) {
      isFirstRender.current = false
      setDarkTheme(dark_mode.get_value())
      return
    }
    dark_mode.set_value(dark_theme)
  }, [dark_theme])

  React.useEffect(() => {
    // If the page has a data-theme attribute (e.g. from pydata-sphinx-theme), use it to set the dark theme
    const page_theme = document.documentElement.dataset.theme
    const params = new URLSearchParams(window.location.search);
    if (page_theme === "dark" || params.get("theme") === "dark") {
      setDarkTheme(true)
    }

    const cb = (val) => setDarkTheme(val)
    if (document.documentElement.dataset.themeManaged === "true") {
      dark_mode.subscribe(cb)
    } else {
      const style_el = document.createElement("style")
      style_el.id = "styles-panel-mui"
      props.view.shadow_el.insertBefore(style_el, props.view.container)
      style_el.textContent = render_theme_css(theme)
    }
    return () => dark_mode.unsubscribe(cb)
  }, [])

  React.useEffect(() => {
    const style_el = props.view.shadow_el.querySelector("#styles-panel-mui")
    if (style_el) {
      style_el.textContent = render_theme_css(theme)
    }
  }, [theme])
  return theme
}

export function isNumber(obj) {
  return toString.call(obj) === "[object Number]"
}

export function apply_flex(view, direction) {
  if (view == null) {
    return
  }
  const sizing = view.box_sizing()
  const flex = (() => {
    const policy = direction == "row" ? sizing.width_policy : sizing.height_policy
    const size = direction == "row" ? sizing.width : sizing.height
    const basis = size != null ? (isNumber(size) ? `${size}px` : value) : "auto"
    switch (policy) {
      case "auto":
      case "fixed": return `0 0 ${basis}`
      case "fit": return "1 1 auto"
      case "min": return "0 1 auto"
      case "max": return "1 0 0px"
    }
  })()

  const align_self = (() => {
    const policy = direction == "row" ? sizing.height_policy : sizing.width_policy
    switch (policy) {
      case "auto":
      case "fixed":
      case "fit":
      case "min": return direction == "row" ? sizing.valign : sizing.halign
      case "max": return "stretch"
    }
  })()

  view.parent_style.replace(":host", {flex, align_self})

  // undo `width/height: 100%` and let `align-self: stretch` do the work
  if (direction == "row") {
    if (sizing.height_policy == "max") {
      view.parent_style.append(":host", {height: "auto"})
    }
  } else {
    if (sizing.width_policy == "max") {
      view.parent_style.append(":host", {width: "auto"})
    }
  }
}

export function findNotebook(el) {
  let feed = null
  while (el) {
    if (el.classList && el.classList.contains("jp-Notebook")) {
      return [el, feed]
    }
    if (el.classList && el.classList.contains("jp-WindowedPanel-outer")) {
      feed = el
    }
    if (el.parentNode) {
      el = el.parentNode
    } else if (el instanceof ShadowRoot) {
      el = el.host
    } else {
      el = null
    }
  }
  return [null, null]
}

// Size parsing function matching FileDropper
function parseSizeString(sizeStr) {
  if (!sizeStr) { return null }
  const match = sizeStr.match(/^(\d+(?:\.\d+)?)\s*(KB|MB|GB)$/i);
  if (!match) { return null }

  const value = parseFloat(match[1])
  const unit = match[2].toUpperCase()

  switch (unit) {
    case "KB": return value * 1024
    case "MB": return value * 1024 * 1024
    case "GB": return value * 1024 * 1024 * 1024
    default: return null
  }
}

// File size validation function
function validateFileSize(file, maxFileSize, maxTotalFileSize, existingFiles = []) {
  const errors = [];

  if (maxFileSize) {
    const maxFileSizeBytes = typeof maxFileSize === "string" ? parseSizeString(maxFileSize) : maxFileSize
    if (maxFileSizeBytes && file.size > maxFileSizeBytes) {
      errors.push(`File "${file.name}" (${formatBytes(file.size)}) exceeds maximum file size of ${formatBytes(maxFileSizeBytes)}`);
    }
  }

  if (maxTotalFileSize) {
    const maxTotalSizeBytes = typeof maxTotalFileSize === "string" ? parseSizeString(maxTotalFileSize) : maxTotalFileSize
    if (maxTotalSizeBytes) {
      const existingSize = existingFiles.reduce((sum, f) => sum + f.size, 0)
      const totalSize = existingSize + file.size
      if (totalSize > maxTotalSizeBytes) {
        errors.push(`Adding "${file.name}" would exceed maximum total size of ${formatBytes(maxTotalSizeBytes)}`)
      }
    }
  }

  return errors;
}

// Format bytes for display
export function formatBytes(bytes) {
  if (bytes === 0) { return "0 B" }
  const k = 1024
  const sizes = ["B", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / k**i).toFixed(2))} ${sizes[i]}`
}

// Chunked upload function using FileDropper's protocol
export async function uploadFileChunked(file, model, chunkSize = 10 * 1024 * 1024) {
  const totalChunks = Math.ceil(file.size / chunkSize);

  for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
    const start = chunkIndex * chunkSize;
    const end = Math.min(start + chunkSize, file.size)
    const chunk = file.slice(start, end)

    // Read chunk as ArrayBuffer
    const arrayBuffer = await new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result)
      reader.onerror = reject
      reader.readAsArrayBuffer(chunk)
    });

    // Send chunk using FileDropper's protocol
    model.send_msg({
      type: "status",
      status: "upload_event",
      chunk: chunkIndex + 1, // 1-indexed
      data: arrayBuffer,
      name: file.name,
      total_chunks: totalChunks,
      mime_type: file.type
    })
  }
}

// New chunked file processing function
export async function processFilesChunked(files, model, maxFileSize, maxTotalFileSize, chunkSize = 10 * 1024 * 1024) {
  try {
    const fileArray = Array.from(files);

    // Validate file sizes on frontend
    for (const file of fileArray) {
      const sizeErrors = validateFileSize(file, model.max_file_size, model.max_total_file_size, fileArray);
      if (sizeErrors.length > 0) {
        throw new Error(sizeErrors.join("; "))
      }
    }

    model.send_msg({status: "initializing", type: "status"})

    // Upload all files using chunked protocol
    for (const file of fileArray) {
      await uploadFileChunked(file, model, chunkSize)
    }

    model.send_msg({status: "finished", type: "status"})
    return fileArray.length
  } catch (error) {
    model.send_msg({status: "error", error: error.message})
    throw error
  }
}

export function isFileAccepted(file, accept) {
  if (!accept || accept.length === 0) {
    return true
  }
  const acceptedTypes = accept.split(",").map(type => type.trim())
  const fileName = file.name
  const fileType = file.type

  return acceptedTypes.some(acceptedType => {
    // Handle file extensions (e.g., ".jpg", ".png")
    if (acceptedType.startsWith(".")) {
      return fileName.toLowerCase().endsWith(acceptedType.toLowerCase())
    }

    // Handle MIME types (e.g., "image/*", "image/jpeg")
    if (acceptedType.includes("/")) {
      if (acceptedType.endsWith("/*")) {
        // Handle wildcard MIME types (e.g., "image/*")
        const baseType = acceptedType.slice(0, -2)
        return fileType.startsWith(baseType)
      } else {
        // Handle exact MIME types (e.g., "image/jpeg")
        return fileType === acceptedType
      }
    }
    return false
  })
}
