#!/usr/bin/env python3
"""Harden WP-002 process identity reuse on the implementation branch."""

from pathlib import Path

KERNEL = Path("crates/turing-kernel/src/lib.rs")
TASK = Path("docs/agent-execution/machine/tasks/TASK-000001.json")
REPORT = Path("docs/research/wp-002-kernel-ipc-2026-07.md")

text = KERNEL.read_text(encoding="utf-8")
if "last_epochs: BTreeMap<ProcessId, ProcessEpoch>" in text:
    raise SystemExit("epoch hardening already applied")

text = text.replace(
    "use std::collections::BTreeMap;\nuse std::collections::btree_map::Entry;\n",
    "use std::collections::BTreeMap;\n",
    1,
)
text = text.replace(
    "    processes: BTreeMap<ProcessId, ProcessPolicy>,\n"
    "    channels: BTreeMap<ChannelId, ChannelState>,\n",
    "    processes: BTreeMap<ProcessId, ProcessPolicy>,\n"
    "    last_epochs: BTreeMap<ProcessId, ProcessEpoch>,\n"
    "    channels: BTreeMap<ChannelId, ChannelState>,\n",
    1,
)
text = text.replace(
    "            processes: BTreeMap::from([(kernel_id, policy)]),\n"
    "            channels: BTreeMap::new(),\n",
    "            processes: BTreeMap::from([(kernel_id, policy)]),\n"
    "            last_epochs: BTreeMap::from([(kernel_id, kernel.epoch())]),\n"
    "            channels: BTreeMap::new(),\n",
    1,
)

old_launch = '''        if self.processes.len() >= MAX_REGISTERED_PROCESSES {
            return Err(KernelError::ProcessTableFull {
                maximum: MAX_REGISTERED_PROCESSES,
            });
        }

        let identity = ProcessIdentity::new(
            child_id,
            ProcessEpoch::new(1).expect("one is a valid process epoch"),
        );
        match self.processes.entry(child_id) {
            Entry::Vacant(entry) => {
                entry.insert(ProcessPolicy {
                    identity,
                    role: child_role,
                    capabilities,
                });
                Ok(identity)
            }
            Entry::Occupied(_) => Err(KernelError::DuplicateProcessId { id: child_id }),
        }
'''
new_launch = '''        if self.processes.contains_key(&child_id) {
            return Err(KernelError::DuplicateProcessId { id: child_id });
        }
        if !self.last_epochs.contains_key(&child_id)
            && self.last_epochs.len() >= MAX_REGISTERED_PROCESSES
        {
            return Err(KernelError::ProcessTableFull {
                maximum: MAX_REGISTERED_PROCESSES,
            });
        }
        let epoch = match self.last_epochs.get(&child_id).copied() {
            Some(last) => last
                .checked_next()
                .ok_or(KernelError::ProcessEpochExhausted { id: child_id })?,
            None => ProcessEpoch::new(1).expect("one is a valid process epoch"),
        };
        let identity = ProcessIdentity::new(child_id, epoch);
        self.processes.insert(
            child_id,
            ProcessPolicy {
                identity,
                role: child_role,
                capabilities,
            },
        );
        self.last_epochs.insert(child_id, epoch);
        Ok(identity)
'''
if old_launch not in text:
    raise SystemExit("launch replacement anchor not found")
text = text.replace(old_launch, new_launch, 1)

old_restart = '''        self.processes.insert(
            current.id(),
            ProcessPolicy {
                identity: next,
                role: policy.role(),
                capabilities: policy.capabilities(),
            },
        );
        self.channels
'''
new_restart = '''        self.processes.insert(
            current.id(),
            ProcessPolicy {
                identity: next,
                role: policy.role(),
                capabilities: policy.capabilities(),
            },
        );
        self.last_epochs.insert(current.id(), next_epoch);
        self.channels
'''
if old_restart not in text:
    raise SystemExit("restart replacement anchor not found")
text = text.replace(old_restart, new_restart, 1)

test_anchor = '''    #[test]
    fn generated_route_and_capability_are_enforced() {
'''
test = '''    #[test]
    fn removed_process_id_uses_a_new_epoch_and_rejects_stale_replay() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let kernel = registry.kernel();
        let renderer = registry
            .launch(
                kernel,
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        let channel = ChannelId::new(1).expect("valid channel");
        registry
            .register_channel(kernel, channel, renderer, kernel)
            .expect("kernel registers channel");
        let stale = envelope(MessageKind::NavigationIntent, renderer, kernel, 1, 1);

        registry
            .remove(kernel, renderer)
            .expect("kernel removes renderer");
        let replacement = registry
            .launch(kernel, renderer.id(), ProcessRole::Renderer)
            .expect("kernel relaunches renderer id");
        assert_eq!(replacement.id(), renderer.id());
        assert!(replacement.epoch() > renderer.epoch());
        registry
            .register_channel(kernel, channel, replacement, kernel)
            .expect("kernel reuses channel for replacement identity");

        assert!(matches!(
            registry.authorize(&stale),
            Err(KernelError::StaleProcess { current, supplied })
                if current == replacement && supplied == renderer
        ));
        let fresh = envelope(MessageKind::NavigationIntent, replacement, kernel, 1, 1);
        registry
            .authorize(&fresh)
            .expect("replacement starts a fresh authenticated sequence");
    }

'''
if test_anchor not in text:
    raise SystemExit("test insertion anchor not found")
text = text.replace(test_anchor, test + test_anchor, 1)
KERNEL.write_text(text, encoding="utf-8")

task = TASK.read_text(encoding="utf-8")
task = task.replace(
    '    "stale process epoch",\n',
    '    "stale process epoch",\n'
    '    "remove and relaunch cannot resurrect a prior process identity",\n',
    1,
)
TASK.write_text(task, encoding="utf-8")

report = REPORT.read_text(encoding="utf-8")
marker = "## Important limitations\n"
note = (
    "## Process-ID reuse hardening\n\n"
    "The kernel retains the last issued epoch for every allocated `ProcessId`, "
    "including removed processes. Relaunching a previously used ID advances the "
    "epoch rather than resetting it, so stale handles and envelopes cannot become "
    "current again when process and channel identifiers are reused. The epoch ledger "
    "is bounded by the generated process-table limit. A regression test covers launch, "
    "channel registration, removal, relaunch, stale replay rejection, and fresh-sequence "
    "acceptance.\n\n"
)
if marker not in report:
    raise SystemExit("report insertion anchor not found")
REPORT.write_text(report.replace(marker, note + marker, 1), encoding="utf-8")
