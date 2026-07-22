# Nova Shell Prototype

Status: development-only source-fidelity and Servo integration proof
Owner: application runtime, UI runtime, engine, platform, accessibility, and developer experience
Last reviewed: 2026-07-22

## Why this exists

The supplied Nova JSX is the browser's intended face. The design-lab header,
background, and presentation canvas were removed from the canonical source so
the Nova root itself owns the browser viewport. This package exists to execute
that source as-is through a low-maintenance, reproducible development path
while the Turing-owned runtime contracts are still being implemented.

This is not a native release shell, a browser compatibility claim, or a
production dependency approval.

## Pipeline

```text
docs/ui-runtime/design-lab/turing-nova-design-source.jsx
  -> pinned esbuild JSX transform
  -> Preact compatibility aliases for react and react-dom
  -> lucide-preact alias for lucide-react imports
  -> bundled browser JavaScript
  -> Servo servoshell desktop window
```

Servo owns the page DOM, CSS parsing, layout, painting, and browser event
delivery in this proof. The package owns only the development launcher,
compatibility aliases, source metadata, and engine-command adapter. The
long-term target remains a Turing-owned JSX runtime; this package is a bridge
for source fidelity, not that runtime.

## Windows prerequisites

- Node.js 18 or newer with npm.
- A locally built Servo `servoshell.exe`. The launcher checks
  `C:\ts\servo\target\debug\servoshell.exe`, then the matching release path.
  Set `TURING_SERVO` to override that location.
- A checkout with the canonical source and the package lockfile present.

## Build and launch

From the repository root:

```powershell
Set-Location apps\nova-shell
npm ci
npm run check
npm run launch:servo
```

`npm run check` rebuilds the ignored `dist/` directory, verifies that the
canonical source is bundled, and writes `dist/build-metadata.json`. The
metadata includes the source SHA-256, byte and line counts, compiler/runtime
versions, output size, and bundle inputs.

To use another Servo checkout:

```powershell
$env:TURING_SERVO = 'C:\path\to\servo\target\debug\servoshell.exe'
npm run launch:servo
```

The launcher opens the generated `dist/index.html` in a visible native Servo
window. It does not start a web server and it does not require a network
connection for the shell itself.

## Engine adapter

`src/entry.jsx` installs the development adapter at
`window.__TURING_ENGINE__`. The adapter accepts versioned commands through:

```js
window.__TURING_ENGINE__.dispatch({
  version: 1,
  type: 'navigation.navigate',
  payload: { query, url, kind },
});
```

The Nova root emits commands for navigation, history, tabs, sidebar state,
reader/split view, URL copy, keyboard input, and every actionable control,
input, and change event. The adapter retains only the last 128 commands for
development inspection through `snapshot()`; it is not a persistence or
authority boundary.

The local component state continues to provide the prototype behavior. A
Rust-owned host must replace the adapter and validate identity, origin,
document epoch, permissions, and command authority before any command can
perform a real browser action.

## Verified behavior

The current proof has been exercised against the local Servo binary on
Windows:

- the bundle builds and the canonical JSX source appears in esbuild metadata;
- Servo headless rendering produced a non-empty screenshot;
- the Nova root filled the viewport without the removed design-lab header or
  outer presentation canvas;
- WebDriver clicked the address surface, typed into the command field, and
  submitted a navigation command through the adapter.

These results prove this bounded development path only. They do not prove
native Turing chrome, real network navigation, profile persistence,
accessibility parity, sandboxing, release packaging, or performance.

## Ownership and AI implementation guidance

Keep visual hierarchy and component composition in the canonical JSX source.
Keep browser authority in Rust contracts and the future host bridge. Do not
add browser behavior directly to the development adapter, silently reintroduce
the design-lab frame, or treat a successful Servo screenshot as native runtime
evidence. Any source change must refresh the design manifest and rerun the
source validator, package check, Servo render proof, and relevant repository
gates.

The next implementation slice is a reviewed Rust host bridge with bounded
command decoding and the same command/state contracts used by the native shell.
