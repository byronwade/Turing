# Graphics foundation decision — lab presenter and its dependencies (2026-07)

Status: accepted for the laboratory presenter only.
Owner: @byronwade.
Recorded from the owner's 2026-07-20 direction to produce a working, visible
browser application; that direction resolves the previously open
`graphics-foundation-review` gate on `WP-009` for this bounded scope, the
same way `docs/research/text-font-foundation-decision-2026-07.md` resolves
the font gate.

## Decision

1. The paint foundation remains the CPU reference rasterizer
   (`turing-raster`, `COMP-017`): opaque sRGB pixels, hard edges, written to
   be read. No GPU interface, tiling, or compositing model is selected.
2. Presentation — putting those pixels in a native window and receiving
   input — is done by a single laboratory binary, `apps/turing-browser`
   (`COMP-022`), using two external crates: `winit` (window and event loop)
   and `softbuffer` (software framebuffer presentation).

## Dependency decision record (per the acceptance policy in
`docs/blueprint-v1/03-language-and-dependency-strategy.md`)

Both crates are maintained by the `rust-windowing` project.

- Functionality, and why no local implementation: window creation, the event
  loop, and framebuffer presentation are operating-system integration, the
  category the independent-engine boundary explicitly permits platform
  primitives for. A local implementation would be thousands of lines of
  platform-specific unsafe FFI in a workspace that forbids unsafe code.
- License: both Apache-2.0/MIT dual-licensed. No patent concerns known.
- Maintenance: `rust-windowing` maintains both across Windows, macOS, X11,
  and Wayland; they are the de-facto standard presentation path for Rust
  GUI work and are releasing actively (winit 0.30.x, softbuffer 0.4.x).
- Transitive surface: resolved by Cargo at ~30 crates on Windows, dominated
  by `windows-sys` bindings. No build-time network access, no codegen
  beyond `cfg` aliasing, no bundled binary blobs.
- Unsafe and native code: both contain platform FFI and are the reason they
  exist; the workspace's own crates remain `forbid(unsafe_code)`, and the
  registry keeps `default_unsafe_policy: forbid` for Turing-owned code.
- Containment: the two crates appear in exactly one binary, which is in
  workspace `members` but not `default-members`, so the default build,
  test, and clippy sweeps stay standard-library-only. No engine crate can
  see a toolkit type; the presenter consumes `turing-engine::Page` through
  its public API and packs pixels. Replacement cost is this one file.
- Security posture: the presenter is not a hostile-input boundary. It loads
  the file named on its own command line; there is no network and no
  navigation to untrusted content.

## What this deliberately does not decide

- The product shell toolkit (`ADR-0013`–`ADR-0016`, `ui-license-review`,
  and the `WP-004` bake-off) — all remain open. This presenter is not a
  candidate in that comparison; it exists so the engine's output is visible
  and clickable while those decisions are made properly.
- Any GPU or compositing foundation. `wgpu`, Vello, and friends remain
  "evaluate" in the technology-stack records.
- Any product support promise. The binary is Research maturity.

## Revocation

Deleting `apps/turing-browser` and the two dependency lines restores a
dependency-free workspace; nothing else references them. If the `WP-004`
bake-off later selects a real toolkit, this presenter is superseded and
should be deleted rather than maintained in parallel.

## Primary sources

- `winit` — https://crates.io/crates/winit, https://github.com/rust-windowing/winit
- `softbuffer` — https://crates.io/crates/softbuffer, https://github.com/rust-windowing/softbuffer
- Transitive dependency count and `windows-sys` binding weight: this
  workspace's own `Cargo.lock`, resolved for `apps/turing-browser`.
