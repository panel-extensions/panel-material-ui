// Builds the panel-material-ui bundle from src/panel_material_ui/index.js.
//
//   node scripts/build.mjs              minified production build
//   node scripts/build.mjs --dev        unminified build
//   node scripts/build.mjs --watch      rebuild on changes
//   node scripts/build.mjs --metafile   also write build/meta.json for size analysis
//
// Two bundles are produced: panel-material-ui.bundle.js, which loads rarely
// used widgets from separate chunks on demand, and panel-material-ui.inline.js,
// a single file for output that inlines the bundle and therefore cannot
// resolve chunks relative to it.
import * as esbuild from "esbuild"
import {mkdir, readdir, rm, writeFile} from "node:fs/promises"
import {fileURLToPath} from "node:url"
import path from "node:path"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const pkg = path.join(root, "src", "panel_material_ui")
const dist = path.join(pkg, "dist")
const entry = path.join(pkg, "index.js")
const args = new Set(process.argv.slice(2))
const dev = args.has("--dev")

const common = {
  absWorkingDir: root,
  bundle: true,
  format: "esm",
  minify: !dev,
  // Production builds of React and MUI, which minify enabled implicitly
  define: {"process.env.NODE_ENV": JSON.stringify(dev ? "development" : "production")},
  loader: {".js": "jsx", ".woff": "file", ".woff2": "file"},
  logLevel: "info",
}

const split = {
  ...common,
  entryPoints: {"panel-material-ui.bundle": entry},
  outdir: dist,
  splitting: true,
  entryNames: "[name]",
  chunkNames: "[name]-[hash]",
  assetNames: "[name]-[hash]",
  metafile: args.has("--metafile"),
}

// The CSS and fonts are identical to those of the split build, so only the
// JS is written
const inline = {
  ...common,
  entryPoints: [entry],
  outdir: dist,
  assetNames: "[name]-[hash]",
  write: false,
  logLevel: "warning",
}

async function writeInline(result) {
  const js = result.outputFiles.find((file) => file.path.endsWith(".js"))
  await writeFile(path.join(dist, "panel-material-ui.inline.js"), js.contents)
}

// Chunks are content hashed, so remove those of previous builds
async function removeChunks() {
  for (const name of await readdir(dist)) {
    if (/-[A-Z0-9]{8}\.js$/.test(name)) {
      await rm(path.join(dist, name))
    }
  }
}

if (args.has("--watch")) {
  const splitCtx = await esbuild.context(split)
  const inlineCtx = await esbuild.context({
    ...inline,
    plugins: [{name: "write-inline", setup(build) { build.onEnd((result) => result.errors.length || writeInline(result)) }}],
  })
  await Promise.all([splitCtx.watch(), inlineCtx.watch()])
} else {
  await removeChunks()
  const result = await esbuild.build(split)
  await writeInline(await esbuild.build(inline))
  if (result.metafile) {
    await mkdir(path.join(root, "build"), {recursive: true})
    await writeFile(path.join(root, "build", "meta.json"), JSON.stringify(result.metafile))
  }
}
