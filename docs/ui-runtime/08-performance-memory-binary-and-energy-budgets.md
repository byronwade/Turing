# Performance, Memory, Binary, and Energy Budgets

Status: measurement contract; numeric targets require baseline evidence  
Owner: UI runtime, performance, build, graphics, and platform

## Budget philosophy

Turing does not set arbitrary marketing numbers before reference prototypes. It defines measured categories, relative gates, and disqualifying architecture costs first; numeric thresholds are accepted after equivalent hardware evidence.

## Hard architecture budgets

- zero additional browser engine or system webview for trusted chrome;
- zero JavaScript or React runtime in the release shell;
- zero runtime HTML/CSS parsing for browser chrome;
- one normal production backend and renderer per package unless a documented fallback is required;
- no eagerly initialized settings, history, DevTools, agent, or Plug-in panels;
- no full-tree rebuild for a local state change where the toolkit can update a bounded subtree;
- no unbounded animation, timer, event, binding, list, image, or diagnostic work;
- all shell allocation and GPU use attributed to a window or shared UI service.

## Measurements

Track stripped binary contribution, compressed package contribution, startup faulted pages, dynamic libraries, cold and warm startup, idle private/physical memory, per-window and per-tab model memory, retained component memory, update allocations, input-to-present latency, frame pacing, GPU allocation, wakeups, energy, hidden-window behavior, suspend/resume, and destruction latency.

## Build experiments

Compare release optimization, Thin/full LTO, codegen units, panic strategy where safe, linker choice, function ordering, split symbols, selected backend features, static/dynamic native dependencies, asset compression, locale packs, icon/vector deduplication, and optional first-party Plug-in packaging.

## Regression rules

A UI framework update cannot land on screenshots alone. It requires before/after raw measurements, component and workflow correctness, accessibility evidence, dependency/unsafe/license diffs, and a rollback path. Empty-window wins do not justify regressions under 100-tab, split-view, IME, accessibility, or renderer-failure workloads.
