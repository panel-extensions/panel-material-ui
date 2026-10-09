// Builds the panel-material-ui bundle from src/panel_material_ui/index.js.
//
//   node scripts/build.mjs              minified production build
//   node scripts/build.mjs --dev        unminified build
//   node scripts/build.mjs --watch      rebuild on changes
//   node scripts/build.mjs --metafile   also write build/meta.json for size analysis
import * as esbuild from "esbuild"
import {fileURLToPath} from "node:url"
import path from "node:path"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const pkg = path.join(root, "src", "panel_material_ui")
const args = new Set(process.argv.slice(2))
const dev = args.has("--dev")

const options = {
  absWorkingDir: root,
  entryPoints: [path.join(pkg, "index.js")],
  outfile: path.join(pkg, "dist", "panel-material-ui.bundle.js"),
  bundle: true,
  format: "esm",
  minify: !dev,
  // Production builds of React and MUI, which minify enabled implicitly
  define: {"process.env.NODE_ENV": JSON.stringify(dev ? "development" : "production")},
  loader: {".js": "jsx", ".woff": "file", ".woff2": "file"},
  metafile: args.has("--metafile"),
  logLevel: "info",
}

if (args.has("--watch")) {
  const ctx = await esbuild.context(options)
  await ctx.watch()
} else {
  const result = await esbuild.build(options)
  if (result.metafile) {
    const {mkdir, writeFile} = await import("node:fs/promises")
    await mkdir(path.join(root, "build"), {recursive: true})
    await writeFile(path.join(root, "build", "meta.json"), JSON.stringify(result.metafile))
  }
}
