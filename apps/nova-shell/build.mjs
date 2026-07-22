import { build, analyzeMetafile } from "esbuild";
import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "../..");
const source = resolve(root, "docs/ui-runtime/design-lab/turing-nova-design-source.jsx");
const tokenSource = resolve(root, "design/tokens.json");
const dist = resolve(here, "dist");
const output = resolve(dist, "nova-shell.js");
const entry = resolve(here, "src/entry.jsx");
const html = resolve(here, "src/index.html");

const sourceBytes = await readFile(source);
const sourceText = sourceBytes.toString("utf8");
const sourceHash = createHash("sha256").update(sourceBytes).digest("hex").toUpperCase();
const tokens = JSON.parse(await readFile(tokenSource, "utf8"));
if (tokens.source !== "docs/ui-runtime/design-lab/turing-nova-design-source.jsx"
  || tokens.source_sha256 !== sourceHash) {
  throw new Error("design/tokens.json is stale or points at a different Nova source");
}

if (process.argv.includes("--clean")) {
  await rm(dist, { recursive: true, force: true });
  process.stdout.write("Nova shell build output removed\n");
  process.exit(0);
}

await mkdir(dist, { recursive: true });
await copyFile(html, resolve(dist, "index.html"));

const result = await build({
  // Resolve dependencies from this package boundary. The Nova source is
  // intentionally outside the package and remains versioned canonical input.
  absWorkingDir: here,
  entryPoints: [entry],
  outfile: output,
  bundle: true,
  format: "iife",
  platform: "browser",
  target: ["es2020"],
  sourcemap: true,
  metafile: true,
  define: {
    "process.env.NODE_ENV": '"production"',
    __TURING_NOVA_SOURCE_SHA256__: JSON.stringify(sourceHash),
    __TURING_NOVA_TOKENS_SHA256__: JSON.stringify(tokens.source_sha256),
  },
  alias: {
    react: resolve(here, "node_modules/preact/compat"),
    "react-dom": resolve(here, "node_modules/preact/compat"),
    "lucide-react": resolve(here, "node_modules/lucide-preact"),
  },
  logLevel: "warning",
});

const metadata = {
  generated_by: "apps/nova-shell/build.mjs",
  source_path: "docs/ui-runtime/design-lab/turing-nova-design-source.jsx",
  source_sha256: sourceHash,
  source_bytes: sourceBytes.length,
  source_lines: sourceText.replace(/\r?\n$/, "").split(/\r?\n/).length,
  compiler: "esbuild 0.28.1",
  runtime: "preact 10.29.7 via preact/compat",
  icons: "lucide-preact 1.25.0",
  design_tokens: {
    path: "design/tokens.json",
    schema_version: tokens.schema_version,
    source_sha256: tokens.source_sha256,
  },
  output_bytes: (await readFile(output)).length,
  bundle_inputs: Object.keys(result.metafile.inputs).sort(),
};

await writeFile(resolve(dist, "build-metadata.json"), `${JSON.stringify(metadata, null, 2)}\n`);

if (process.argv.includes("--check")) {
  const analysis = await analyzeMetafile(result.metafile, { verbose: false });
  if (!analysis.includes("preact")) {
    throw new Error("Nova bundle does not contain the expected Preact runtime");
  }
  if (!analysis.includes("turing-nova-design-source.jsx")) {
    throw new Error("Nova bundle does not contain the canonical source artifact");
  }
  if (metadata.design_tokens.source_sha256 !== metadata.source_sha256) {
    throw new Error("Nova bundle metadata has stale design-token provenance");
  }
}

process.stdout.write(
  `Nova shell built: ${metadata.output_bytes} bytes, source ${sourceHash}\n`,
);
