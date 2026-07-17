# Windowing, Input, IME, Accessibility, and Platform Semantics

Status: platform integration plan  
Owner: UI runtime, platform, text/input, and accessibility

## Reference platform

Select one M1 reference desktop platform before implementing three full adapters. The architecture remains portable, but the first platform must prove window lifecycle, menus, text input, IME, clipboard, drag/drop, accessibility, page-surface composition, packaging, sandbox interaction, and crash recovery end to end.

## Required platform contracts

- window identity, ownership, visibility, occlusion, scale, display, full-screen, and close negotiation;
- native menu, shortcut, command, notification, default-browser, and external-protocol behavior;
- pointer, wheel, touch/pen where supported, gesture, keyboard, dead-key, composition, candidate-window, selection, and text services;
- clipboard data types, drag/drop offers, file handles, and profile-aware security policy;
- system appearance, high contrast, reduced motion, text scaling, power state, sleep/resume, and memory pressure;
- accessibility roles, names, values, relations, actions, focus, bounds, live regions, tables, trees, and text ranges.

## Toolkit acceptance

A toolkit’s generic accessibility claim is insufficient. Turing tests VoiceOver, UI Automation with Narrator/NVDA, and AT-SPI/Orca as appropriate. IME is tested with representative East Asian, Indic, bidirectional, dead-key, emoji, and composition workflows.

## Trusted surfaces

Origin, profile, private mode, credential, permission, capture, agent confirmation, update, and crash-recovery UI cannot be rendered inside page content or styled by pages. Toolkit popovers and overlays must remain inside trusted stacking and input regions.

## Portability rule

Platform-specific behavior stays behind semantic contracts. Business logic does not branch on raw OS handles. Unsupported platform capabilities are declared and tested rather than silently approximated.
