#!/usr/bin/env python3
"""Apply the final WP-002 channel-ownership and queue-accounting hardening."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_exact(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"{relative}: expected replacement anchor not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(relative: str, marker: str, content: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


# Freeze each queue charge at admission rather than recomputing EncodedSize
# during dequeue, where mutable or non-idempotent payload behavior could corrupt
# accounting or trigger an internal subtraction failure.
replace_exact(
    "crates/turing-ipc/src/queue.rs",
    "    items: VecDeque<T>,",
    "    items: VecDeque<(usize, T)>,",
)
replace_exact(
    "crates/turing-ipc/src/queue.rs",
    """        self.items.push_back(item);
        self.queued_bytes = next_bytes;
        Ok(())
""",
    """        self.items.push_back((incoming, item));
        self.queued_bytes = next_bytes;
        Ok(())
""",
)
replace_exact(
    "crates/turing-ipc/src/queue.rs",
    """        let item = self.items.pop_front()?;
        self.queued_bytes = self
            .queued_bytes
            .checked_sub(item.encoded_len())
            .expect("queued byte accounting is internally consistent");
        Some(item)
""",
    """        let (charged_bytes, item) = self.items.pop_front()?;
        self.queued_bytes = self
            .queued_bytes
            .checked_sub(charged_bytes)
            .expect("queued byte accounting is internally consistent");
        Some(item)
""",
)
replace_exact(
    "crates/turing-ipc/src/queue.rs",
    "    use super::{BoundedQueue, QueueErrorKind};\n",
    "    use std::cell::Cell;\n\n    use super::{BoundedQueue, QueueErrorKind};\n",
)
replace_exact(
    "crates/turing-ipc/src/queue.rs",
    """    #[test]
    fn releases_byte_charge_when_item_is_popped() {
        let mut queue = BoundedQueue::new(QueueClass::Control);
        queue.try_push(SizedItem(32)).expect("item fits");
        assert_eq!(queue.queued_bytes(), 32);
        assert_eq!(queue.pop_front(), Some(SizedItem(32)));
        assert_eq!(queue.queued_bytes(), 0);
    }
}
""",
    """    #[test]
    fn releases_byte_charge_when_item_is_popped() {
        let mut queue = BoundedQueue::new(QueueClass::Control);
        queue.try_push(SizedItem(32)).expect("item fits");
        assert_eq!(queue.queued_bytes(), 32);
        assert_eq!(queue.pop_front(), Some(SizedItem(32)));
        assert_eq!(queue.queued_bytes(), 0);
    }

    #[derive(Debug)]
    struct ChangingSize(Cell<usize>);

    impl EncodedSize for ChangingSize {
        fn encoded_len(&self) -> usize {
            let current = self.0.get();
            self.0.set(current + 1);
            current
        }
    }

    #[test]
    fn dequeue_uses_the_charge_captured_at_admission() {
        let mut queue = BoundedQueue::new(QueueClass::Control);
        queue
            .try_push(ChangingSize(Cell::new(32)))
            .expect("item fits");
        assert_eq!(queue.queued_bytes(), 32);
        let item = queue.pop_front().expect("item remains available");
        assert_eq!(item.0.get(), 33, "encoded size was queried only at admission");
        assert_eq!(queue.queued_bytes(), 0);
    }
}
""",
)

# Channel IDs are broker-created resources. An untrusted message may reference
# an existing channel but can never establish a new endpoint binding.
replace_exact(
    "crates/turing-kernel/src/lib.rs",
    """    /// The channel table reached its fixed M0 limit.
    ChannelTableFull {
        /// Maximum channel records.
        maximum: usize,
    },
    /// A channel ID was reused for different process endpoints.
""",
    """    /// The channel table reached its fixed M0 limit.
    ChannelTableFull {
        /// Maximum channel records.
        maximum: usize,
    },
    /// No broker-registered channel exists for the supplied ID.
    UnknownChannel {
        /// Unknown channel identity.
        channel: ChannelId,
    },
    /// A channel ID is already registered.
    DuplicateChannelId {
        /// Duplicate channel identity.
        channel: ChannelId,
    },
    /// A channel ID was reused for different process endpoints.
""",
)
replace_exact(
    "crates/turing-kernel/src/lib.rs",
    """            Self::ChannelTableFull { maximum } => {
                write!(formatter, "channel table reached its limit of {maximum}")
            }
            Self::ChannelEndpointMismatch { channel } => {
""",
    """            Self::ChannelTableFull { maximum } => {
                write!(formatter, "channel table reached its limit of {maximum}")
            }
            Self::UnknownChannel { channel } => {
                write!(formatter, "channel {channel} is not registered")
            }
            Self::DuplicateChannelId { channel } => {
                write!(formatter, "channel {channel} is already registered")
            }
            Self::ChannelEndpointMismatch { channel } => {
""",
)
replace_exact(
    "crates/turing-kernel/src/lib.rs",
    """    /// Authenticates endpoints, route, capability, channel binding, and sequence.
    pub fn authorize<T>(
""",
    """    /// Registers one channel through a process-broker capability.
    ///
    /// Channel identity is never established from an untrusted envelope. A future
    /// operating-system transport must bind its authenticated endpoints to this
    /// broker-created record before delivering control messages.
    pub fn register_channel(
        &mut self,
        broker: ProcessIdentity,
        channel: ChannelId,
        sender: ProcessIdentity,
        receiver: ProcessIdentity,
    ) -> Result<(), KernelError> {
        let broker_policy = self.policy(broker)?;
        if !broker_policy.allows(Capability::ProcessBroker) {
            return Err(KernelError::MissingCapability {
                role: broker_policy.role(),
                capability: Capability::ProcessBroker,
            });
        }
        self.policy(sender)?;
        self.policy(receiver)?;
        if self.channels.contains_key(&channel) {
            return Err(KernelError::DuplicateChannelId { channel });
        }
        if self.channels.len() >= MAX_REGISTERED_CHANNELS {
            return Err(KernelError::ChannelTableFull {
                maximum: MAX_REGISTERED_CHANNELS,
            });
        }
        self.channels.insert(
            channel,
            ChannelState {
                sender,
                receiver,
                sequence: SequenceTracker::new(),
            },
        );
        Ok(())
    }

    /// Authenticates endpoints, route, capability, channel binding, and sequence.
    pub fn authorize<T>(
""",
)
replace_exact(
    "crates/turing-kernel/src/lib.rs",
    """        let channel_id = envelope.channel();
        if !self.channels.contains_key(&channel_id)
            && self.channels.len() >= MAX_REGISTERED_CHANNELS
        {
            return Err(KernelError::ChannelTableFull {
                maximum: MAX_REGISTERED_CHANNELS,
            });
        }

        let channel = self.channels.entry(channel_id).or_insert(ChannelState {
            sender: envelope.sender(),
            receiver: envelope.receiver(),
            sequence: SequenceTracker::new(),
        });
""",
    """        let channel_id = envelope.channel();
        let Some(channel) = self.channels.get_mut(&channel_id) else {
            return Err(KernelError::UnknownChannel {
                channel: channel_id,
            });
        };
""",
)

# The shell must obtain a broker-created channel before using it.
replace_exact(
    "apps/turing-shell/src/main.rs",
    """    let renderer = registry.launch(kernel, ProcessId::new(2)?, ProcessRole::Renderer)?;
    let message = ControlEnvelope::new(
""",
    """    let renderer = registry.launch(kernel, ProcessId::new(2)?, ProcessRole::Renderer)?;
    let channel = ChannelId::new(1)?;
    registry.register_channel(kernel, channel, renderer, kernel)?;
    let message = ControlEnvelope::new(
""",
)
replace_exact(
    "apps/turing-shell/src/main.rs",
    "        ChannelId::new(1)?,\n",
    "        channel,\n",
)

# Replace the existing channel test with explicit registration and add negative
# coverage for unknown and unauthorized channels.
replace_exact(
    "crates/turing-kernel/src/lib.rs",
    """    #[test]
    fn channel_sequence_and_endpoint_binding_are_enforced() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let renderer = registry
            .launch(
                registry.kernel(),
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        let first = envelope(
            MessageKind::NavigationIntent,
            renderer,
            registry.kernel(),
            1,
            1,
        );
        registry.authorize(&first).expect("first message is valid");
        let duplicate = envelope(
            MessageKind::NavigationIntent,
            renderer,
            registry.kernel(),
            1,
            1,
        );
        assert!(matches!(
            registry.authorize(&duplicate),
            Err(KernelError::Sequence(_))
        ));
    }
}
""",
    """    #[test]
    fn unregistered_channel_is_rejected() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let kernel = registry.kernel();
        let renderer = registry
            .launch(
                kernel,
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        let message = envelope(MessageKind::NavigationIntent, renderer, kernel, 1, 1);
        assert_eq!(
            registry.authorize(&message),
            Err(KernelError::UnknownChannel {
                channel: ChannelId::new(1).expect("valid channel"),
            })
        );
    }

    #[test]
    fn renderer_cannot_register_a_channel() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let kernel = registry.kernel();
        let renderer = registry
            .launch(
                kernel,
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        assert_eq!(
            registry.register_channel(
                renderer,
                ChannelId::new(1).expect("valid channel"),
                renderer,
                kernel,
            ),
            Err(KernelError::MissingCapability {
                role: ProcessRole::Renderer,
                capability: Capability::ProcessBroker,
            })
        );
    }

    #[test]
    fn channel_sequence_and_endpoint_binding_are_enforced() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let kernel = registry.kernel();
        let renderer = registry
            .launch(
                kernel,
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        let other_renderer = registry
            .launch(
                kernel,
                ProcessId::new(3).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches second renderer");
        let channel = ChannelId::new(1).expect("valid channel");
        registry
            .register_channel(kernel, channel, renderer, kernel)
            .expect("kernel registers channel");
        let first = envelope(MessageKind::NavigationIntent, renderer, kernel, 1, 1);
        registry.authorize(&first).expect("first message is valid");
        let duplicate = envelope(MessageKind::NavigationIntent, renderer, kernel, 1, 1);
        assert!(matches!(
            registry.authorize(&duplicate),
            Err(KernelError::Sequence(_))
        ));
        let mismatched = envelope(
            MessageKind::NavigationIntent,
            other_renderer,
            kernel,
            1,
            2,
        );
        assert_eq!(
            registry.authorize(&mismatched),
            Err(KernelError::ChannelEndpointMismatch { channel })
        );
        assert_eq!(
            registry.register_channel(kernel, channel, renderer, kernel),
            Err(KernelError::DuplicateChannelId { channel })
        );
    }
}
""",
)

# Synchronize the execution task.
task_path = ROOT / "docs/agent-execution/machine/tasks/TASK-000001.json"
task = json.loads(task_path.read_text(encoding="utf-8"))
for criterion in [
    "only a process-broker principal can register a channel before messages use it",
    "queue byte accounting uses the immutable charge captured at admission",
]:
    if criterion not in task["acceptance_criteria"]:
        task["acceptance_criteria"].append(criterion)
for test in [
    "unregistered channel",
    "unauthorized channel registration",
    "duplicate channel registration",
    "mutable encoded-size accounting",
]:
    if test not in task["negative_tests"]:
        task["negative_tests"].append(test)
task_path.write_text(json.dumps(task, indent=2) + "\n", encoding="utf-8")

# Evidence and policy prose.
replace_exact(
    "docs/research/wp-002-kernel-ipc-2026-07.md",
    "`BoundedQueue` applies both generated item-count and encoded-byte budgets. `try_push` never blocks, evicts, or drops silently. Rejected work and its reason are returned to the caller. Dequeue releases the exact byte charge.\n",
    "`BoundedQueue` applies both generated item-count and encoded-byte budgets. `try_push` never blocks, evicts, or drops silently. Rejected work and its reason are returned to the caller. The queue stores the byte charge at admission and releases that stored value on dequeue, so mutable or non-idempotent `EncodedSize` behavior cannot corrupt accounting or trigger an internal subtraction failure.\n",
)
replace_exact(
    "docs/research/wp-002-kernel-ipc-2026-07.md",
    "- caps registered processes and channels;\n- restarts children with a new process epoch;\n",
    "- caps registered processes and channels;\n- permits channel creation only through an authenticated process-broker capability;\n- rejects envelopes using an unregistered channel rather than allowing a sender to claim an ID implicitly;\n- restarts children with a new process epoch;\n",
)
replace_exact(
    "docs/research/wp-002-kernel-ipc-2026-07.md",
    "- byte-charge release on dequeue;\n",
    "- immutable admission-charge release on dequeue, including a mutable-size regression case;\n",
)
replace_exact(
    "docs/research/wp-002-kernel-ipc-2026-07.md",
    "- channel sequence enforcement;\n",
    "- broker-only channel registration, unknown-channel rejection, duplicate registration denial, endpoint binding, and sequence enforcement;\n",
)
replace_exact(
    "docs/research/wp-002-kernel-ipc-2026-07.md",
    "- A channel cannot silently switch endpoints.\n- Message, queue, process, and channel resources are bounded.\n",
    "- An envelope cannot create a channel; a process-broker principal must register its authenticated endpoints first.\n- A channel cannot silently switch endpoints.\n- Queue accounting uses the charge captured before admission rather than trusting later payload behavior.\n- Message, queue, process, and channel resources are bounded.\n",
)
replace_exact(
    "docs/research/wp-002-kernel-ipc-2026-07.md",
    "- peer authentication on Unix sockets, Windows ALPC/named pipes, Mach IPC, or another transport;\n",
    "- peer authentication on Unix sockets, Windows ALPC/named pipes, Mach IPC, or another transport, including binding the authenticated transport to the broker-registered channel;\n",
)
replace_exact(
    "docs/blueprint-v1/04-system-architecture.md",
    "`turing-types::ProcessIdentity` combines a stable process ID with a monotonic restart epoch. `turing-kernel::ProcessRegistry` is the deterministic authorization oracle for launch, capability attenuation, stale-process rejection, route validation, channel endpoint binding, and exact sequence state. `turing-ipc` supplies bounded envelopes and explicit count/byte backpressure.\n",
    "`turing-types::ProcessIdentity` combines a stable process ID with a monotonic restart epoch. `turing-kernel::ProcessRegistry` is the deterministic authorization oracle for launch, capability attenuation, stale-process rejection, route validation, broker-only channel registration, endpoint binding, and exact sequence state. `turing-ipc` supplies bounded envelopes and explicit count/byte backpressure whose byte charge is frozen at admission.\n",
)
replace_exact(
    "docs/blueprint-v1/08-security-and-sandbox.md",
    "The `WP-002` reference establishes deny-by-default generated role/capability policy, restart-safe process epochs, capability attenuation without escalation, explicit message routes, kind-specific size and document-epoch checks, channel endpoint binding, exact monotonic sequence validation, bounded process/channel tables, and bounded queues that return rejected work instead of silently dropping it.\n",
    "The `WP-002` reference establishes deny-by-default generated role/capability policy, restart-safe process epochs, capability attenuation without escalation, explicit message routes, kind-specific size and document-epoch checks, process-broker-only channel registration, unknown-channel rejection, endpoint binding, exact monotonic sequence validation, bounded process/channel tables, and bounded queues that return rejected work instead of silently dropping it. Queue byte accounting uses the immutable admission charge rather than recomputing a potentially mutable payload value.\n",
)
replace_exact(
    "docs/blueprint-v1/09-performance-memory.md",
    "The generated control-plane schema now defines queue classes with both item-count and encoded-byte ceilings. `turing-ipc::BoundedQueue` applies explicit non-blocking backpressure, never silently evicts or drops work, returns rejected items to the caller, and reconciles byte charge on dequeue. Message kinds also carry generated encoded-size ceilings.\n",
    "The generated control-plane schema now defines queue classes with both item-count and encoded-byte ceilings. `turing-ipc::BoundedQueue` applies explicit non-blocking backpressure, never silently evicts or drops work, returns rejected items to the caller, stores the admitted byte charge beside the item, and releases that exact charge on dequeue. Message kinds also carry generated encoded-size ceilings.\n",
)
replace_exact(
    "docs/blueprint-v1/12-testing-compatibility.md",
    "CI now checks that the canonical IPC schema is valid and that committed Rust and process-capability documentation regenerate byte-for-byte. Unit and integration tests cover identity epochs, message limits, document scope, sequence gaps and duplicates, queue backpressure, launch denial, capability escalation, stale identities, denied routes, attenuated capabilities, channel endpoint binding, and shell-level authorization.\n",
    "CI now checks that the canonical IPC schema is valid and that committed Rust and process-capability documentation regenerate byte-for-byte. Unit and integration tests cover identity epochs, message limits, document scope, sequence gaps and duplicates, queue backpressure, immutable admission-charge accounting, launch denial, capability escalation, stale identities, denied routes, attenuated capabilities, broker-only channel registration, unknown and duplicate channels, endpoint binding, and shell-level authorization.\n",
)
replace_exact(
    "README.md",
    "- bounded envelopes, exact channel sequence validation, explicit queue backpressure, and no silent eviction;\n",
    "- bounded envelopes, broker-registered channels, exact channel sequence validation, stable admission-time queue charging, explicit backpressure, and no silent eviction;\n",
)
append_once(
    "docs/research-log.md",
    "<!-- WP-002-AUDIT-HARDENING-2026-07 -->",
    """<!-- WP-002-AUDIT-HARDENING-2026-07 -->
## 2026-07-17 — WP-002 channel and queue audit hardening

A final non-approving audit found that the first envelope could implicitly claim an unused channel ID and that generic queue accounting recomputed `EncodedSize` during dequeue. The reference now requires process-broker registration before a channel can carry messages, rejects unknown and duplicate channel use, and stores the byte charge captured at admission. Negative tests and all affected architecture, security, performance, testing, task, and evidence records were synchronized. The change remains an M0 reference and does not add an operating-system transport or production-security claim.""",
)
