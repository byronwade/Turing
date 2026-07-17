// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use core::fmt;
use std::collections::BTreeMap;
use std::collections::btree_map::Entry;

pub use turing_ipc::{Capability, MessageKind, ProcessRole};
use turing_ipc::{ControlEnvelope, MAX_REGISTERED_PROCESSES, SequenceError, SequenceTracker};
use turing_types::{ChannelId, ProcessEpoch, ProcessId, ProcessIdentity};

/// Maximum active control channels in the M0 kernel reference model.
pub const MAX_REGISTERED_CHANNELS: usize = 4096;

/// Compact set of explicit process capabilities.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct CapabilitySet(u128);

impl CapabilitySet {
    /// Empty capability set.
    pub const EMPTY: Self = Self(0);

    /// Returns the generated default capability set for a role.
    #[must_use]
    pub const fn for_role(role: ProcessRole) -> Self {
        Self(role.default_capability_bits())
    }

    /// Inserts one capability.
    #[must_use]
    pub const fn with(self, capability: Capability) -> Self {
        Self(self.0 | (1_u128 << capability as u8))
    }

    /// Removes one capability.
    #[must_use]
    pub const fn without(self, capability: Capability) -> Self {
        Self(self.0 & !(1_u128 << capability as u8))
    }

    /// Returns whether the capability is present.
    #[must_use]
    pub const fn contains(self, capability: Capability) -> bool {
        self.0 & (1_u128 << capability as u8) != 0
    }

    /// Returns whether every capability is contained by another set.
    #[must_use]
    pub const fn is_subset_of(self, other: Self) -> bool {
        self.0 & !other.0 == 0
    }
}

/// One current process identity, role, and attenuated capability assignment.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ProcessPolicy {
    identity: ProcessIdentity,
    role: ProcessRole,
    capabilities: CapabilitySet,
}

impl ProcessPolicy {
    /// Creates the generated default policy for one process role.
    #[must_use]
    pub const fn for_role(identity: ProcessIdentity, role: ProcessRole) -> Self {
        Self {
            identity,
            role,
            capabilities: CapabilitySet::for_role(role),
        }
    }

    /// Returns the restart-safe process identity.
    #[must_use]
    pub const fn identity(self) -> ProcessIdentity {
        self.identity
    }

    /// Returns the process role.
    #[must_use]
    pub const fn role(self) -> ProcessRole {
        self.role
    }

    /// Returns the explicit capability set.
    #[must_use]
    pub const fn capabilities(self) -> CapabilitySet {
        self.capabilities
    }

    /// Returns whether this process may exercise a capability.
    #[must_use]
    pub const fn allows(self, capability: Capability) -> bool {
        self.capabilities.contains(capability)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct ChannelState {
    sender: ProcessIdentity,
    receiver: ProcessIdentity,
    sequence: SequenceTracker,
}

/// Successful kernel authorization result for one envelope.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct AuthorizedRoute {
    sender_role: ProcessRole,
    receiver_role: ProcessRole,
    required_capability: Option<Capability>,
}

impl AuthorizedRoute {
    /// Returns the authenticated sender role.
    #[must_use]
    pub const fn sender_role(self) -> ProcessRole {
        self.sender_role
    }

    /// Returns the authenticated receiver role.
    #[must_use]
    pub const fn receiver_role(self) -> ProcessRole {
        self.receiver_role
    }

    /// Returns the capability required by the generated message schema.
    #[must_use]
    pub const fn required_capability(self) -> Option<Capability> {
        self.required_capability
    }
}

/// Error returned by process registration or message authorization.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum KernelError {
    /// The process table reached its fixed M0 limit.
    ProcessTableFull {
        /// Maximum process records.
        maximum: usize,
    },
    /// A process ID is already assigned to a live process.
    DuplicateProcessId {
        /// Reused process ID.
        id: ProcessId,
    },
    /// No process with the supplied stable ID is registered.
    UnknownProcess {
        /// Unknown process ID.
        id: ProcessId,
    },
    /// The process ID exists, but the supplied restart epoch is stale.
    StaleProcess {
        /// Current registered identity.
        current: ProcessIdentity,
        /// Identity supplied by the caller.
        supplied: ProcessIdentity,
    },
    /// The parent role cannot launch the requested child role.
    LaunchDenied {
        /// Parent role.
        parent: ProcessRole,
        /// Requested child role.
        child: ProcessRole,
    },
    /// Requested capabilities exceed the generated role defaults.
    CapabilityEscalation {
        /// Child role whose defaults were exceeded.
        role: ProcessRole,
    },
    /// The process lacks a capability required by the message schema.
    MissingCapability {
        /// Authenticated sender role.
        role: ProcessRole,
        /// Required capability.
        capability: Capability,
    },
    /// The generated message schema denies the role pair.
    RouteDenied {
        /// Message kind.
        kind: MessageKind,
        /// Authenticated sender role.
        sender: ProcessRole,
        /// Authenticated receiver role.
        receiver: ProcessRole,
    },
    /// The channel table reached its fixed M0 limit.
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
    ChannelEndpointMismatch {
        /// Channel identity.
        channel: ChannelId,
    },
    /// A receive-side sequence check failed.
    Sequence(SequenceError),
    /// A process restart epoch exhausted its integer space.
    ProcessEpochExhausted {
        /// Process whose epoch cannot advance.
        id: ProcessId,
    },
    /// The browser kernel cannot be restarted through the child-process API.
    KernelRestartDenied,
}

impl fmt::Display for KernelError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::ProcessTableFull { maximum } => {
                write!(formatter, "process table reached its limit of {maximum}")
            }
            Self::DuplicateProcessId { id } => write!(formatter, "process {id} already exists"),
            Self::UnknownProcess { id } => write!(formatter, "process {id} is not registered"),
            Self::StaleProcess { current, supplied } => {
                write!(
                    formatter,
                    "stale process identity {supplied}; current is {current}"
                )
            }
            Self::LaunchDenied { parent, child } => write!(
                formatter,
                "{} cannot launch {}",
                parent.as_str(),
                child.as_str()
            ),
            Self::CapabilityEscalation { role } => {
                write!(formatter, "capabilities exceed {} defaults", role.as_str())
            }
            Self::MissingCapability { role, capability } => write!(
                formatter,
                "{} lacks required capability {}",
                role.as_str(),
                capability.as_str()
            ),
            Self::RouteDenied {
                kind,
                sender,
                receiver,
            } => write!(
                formatter,
                "{} route {} -> {} is denied",
                kind.as_str(),
                sender.as_str(),
                receiver.as_str()
            ),
            Self::ChannelTableFull { maximum } => {
                write!(formatter, "channel table reached its limit of {maximum}")
            }
            Self::UnknownChannel { channel } => {
                write!(formatter, "channel {channel} is not registered")
            }
            Self::DuplicateChannelId { channel } => {
                write!(formatter, "channel {channel} is already registered")
            }
            Self::ChannelEndpointMismatch { channel } => {
                write!(
                    formatter,
                    "channel {channel} is bound to different endpoints"
                )
            }
            Self::Sequence(error) => error.fmt(formatter),
            Self::ProcessEpochExhausted { id } => {
                write!(formatter, "process {id} exhausted its restart epoch")
            }
            Self::KernelRestartDenied => {
                formatter.write_str("browser kernel restart is not a child-process operation")
            }
        }
    }
}

impl std::error::Error for KernelError {}

impl From<SequenceError> for KernelError {
    fn from(error: SequenceError) -> Self {
        Self::Sequence(error)
    }
}

/// In-memory reference model for process identity and control-message policy.
///
/// This is not an operating-system process launcher or transport. It is the
/// deterministic policy oracle that future platform launchers and IPC
/// transports must match.
#[derive(Debug)]
pub struct ProcessRegistry {
    kernel: ProcessIdentity,
    processes: BTreeMap<ProcessId, ProcessPolicy>,
    channels: BTreeMap<ChannelId, ChannelState>,
}

impl ProcessRegistry {
    /// Creates a registry containing the single privileged browser kernel.
    #[must_use]
    pub fn new(kernel_id: ProcessId) -> Self {
        let kernel = ProcessIdentity::new(
            kernel_id,
            ProcessEpoch::new(1).expect("one is a valid process epoch"),
        );
        let policy = ProcessPolicy::for_role(kernel, ProcessRole::BrowserKernel);
        Self {
            kernel,
            processes: BTreeMap::from([(kernel_id, policy)]),
            channels: BTreeMap::new(),
        }
    }

    /// Returns the current browser-kernel identity.
    #[must_use]
    pub const fn kernel(&self) -> ProcessIdentity {
        self.kernel
    }

    /// Returns the current process policy when the full identity is valid.
    pub fn policy(&self, identity: ProcessIdentity) -> Result<ProcessPolicy, KernelError> {
        let Some(policy) = self.processes.get(&identity.id()).copied() else {
            return Err(KernelError::UnknownProcess { id: identity.id() });
        };
        if policy.identity() != identity {
            return Err(KernelError::StaleProcess {
                current: policy.identity(),
                supplied: identity,
            });
        }
        Ok(policy)
    }

    /// Launches a child with the generated default capabilities for its role.
    pub fn launch(
        &mut self,
        parent: ProcessIdentity,
        child_id: ProcessId,
        child_role: ProcessRole,
    ) -> Result<ProcessIdentity, KernelError> {
        self.launch_with_capabilities(
            parent,
            child_id,
            child_role,
            CapabilitySet::for_role(child_role),
        )
    }

    /// Launches a child with an attenuated subset of its generated defaults.
    pub fn launch_with_capabilities(
        &mut self,
        parent: ProcessIdentity,
        child_id: ProcessId,
        child_role: ProcessRole,
        capabilities: CapabilitySet,
    ) -> Result<ProcessIdentity, KernelError> {
        let parent_policy = self.policy(parent)?;
        if !parent_policy.role().may_launch(child_role) {
            return Err(KernelError::LaunchDenied {
                parent: parent_policy.role(),
                child: child_role,
            });
        }
        if !capabilities.is_subset_of(CapabilitySet::for_role(child_role)) {
            return Err(KernelError::CapabilityEscalation { role: child_role });
        }
        if self.processes.len() >= MAX_REGISTERED_PROCESSES {
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
    }

    /// Restarts a child process with the same role and attenuated capabilities.
    pub fn restart(
        &mut self,
        parent: ProcessIdentity,
        current: ProcessIdentity,
    ) -> Result<ProcessIdentity, KernelError> {
        let parent_policy = self.policy(parent)?;
        if !parent_policy.allows(Capability::ProcessBroker) {
            return Err(KernelError::MissingCapability {
                role: parent_policy.role(),
                capability: Capability::ProcessBroker,
            });
        }
        if current == self.kernel {
            return Err(KernelError::KernelRestartDenied);
        }
        let policy = self.policy(current)?;
        let next_epoch = current
            .epoch()
            .checked_next()
            .ok_or(KernelError::ProcessEpochExhausted { id: current.id() })?;
        let next = ProcessIdentity::new(current.id(), next_epoch);
        self.processes.insert(
            current.id(),
            ProcessPolicy {
                identity: next,
                role: policy.role(),
                capabilities: policy.capabilities(),
            },
        );
        self.channels
            .retain(|_, channel| channel.sender != current && channel.receiver != current);
        Ok(next)
    }

    /// Removes a child process and every channel bound to its identity.
    pub fn remove(
        &mut self,
        parent: ProcessIdentity,
        current: ProcessIdentity,
    ) -> Result<(), KernelError> {
        let parent_policy = self.policy(parent)?;
        if !parent_policy.allows(Capability::ProcessBroker) {
            return Err(KernelError::MissingCapability {
                role: parent_policy.role(),
                capability: Capability::ProcessBroker,
            });
        }
        if current == self.kernel {
            return Err(KernelError::KernelRestartDenied);
        }
        self.policy(current)?;
        self.processes.remove(&current.id());
        self.channels
            .retain(|_, channel| channel.sender != current && channel.receiver != current);
        Ok(())
    }

    /// Registers one channel through a process-broker capability.
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
        &mut self,
        envelope: &ControlEnvelope<T>,
    ) -> Result<AuthorizedRoute, KernelError> {
        let sender = self.policy(envelope.sender())?;
        let receiver = self.policy(envelope.receiver())?;
        let kind = envelope.kind();
        if !kind.allows_route(sender.role(), receiver.role()) {
            return Err(KernelError::RouteDenied {
                kind,
                sender: sender.role(),
                receiver: receiver.role(),
            });
        }
        let required_capability = kind.required_capability();
        if let Some(capability) = required_capability
            && !sender.allows(capability)
        {
            return Err(KernelError::MissingCapability {
                role: sender.role(),
                capability,
            });
        }

        let channel_id = envelope.channel();
        let Some(channel) = self.channels.get_mut(&channel_id) else {
            return Err(KernelError::UnknownChannel {
                channel: channel_id,
            });
        };
        if channel.sender != envelope.sender() || channel.receiver != envelope.receiver() {
            return Err(KernelError::ChannelEndpointMismatch {
                channel: channel_id,
            });
        }
        channel.sequence.accept(envelope.sequence())?;

        Ok(AuthorizedRoute {
            sender_role: sender.role(),
            receiver_role: receiver.role(),
            required_capability,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::{Capability, CapabilitySet, KernelError, ProcessRegistry, ProcessRole};
    use turing_ipc::{ControlEnvelope, MessageKind};
    use turing_types::{
        ChannelId, DocumentEpoch, OperationId, ProcessId, ProcessIdentity, SequenceNumber,
    };

    fn envelope(
        kind: MessageKind,
        sender: ProcessIdentity,
        receiver: ProcessIdentity,
        channel: u64,
        sequence: u64,
    ) -> ControlEnvelope<()> {
        ControlEnvelope::new(
            kind,
            sender,
            receiver,
            ChannelId::new(channel).expect("valid channel"),
            SequenceNumber::new(sequence).expect("valid sequence"),
            OperationId::new(sequence).expect("valid operation"),
            Some(DocumentEpoch::new(1).expect("valid document epoch")),
            64,
            (),
        )
        .expect("valid test envelope")
    }

    #[test]
    fn renderer_cannot_launch_processes() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let renderer = registry
            .launch(
                registry.kernel(),
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        assert_eq!(
            registry.launch(
                renderer,
                ProcessId::new(3).expect("valid process id"),
                ProcessRole::Network,
            ),
            Err(KernelError::LaunchDenied {
                parent: ProcessRole::Renderer,
                child: ProcessRole::Network,
            })
        );
    }

    #[test]
    fn launch_capabilities_can_only_be_attenuated() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let escalated =
            CapabilitySet::for_role(ProcessRole::Renderer).with(Capability::NetworkSockets);
        assert_eq!(
            registry.launch_with_capabilities(
                registry.kernel(),
                ProcessId::new(2).expect("valid process id"),
                ProcessRole::Renderer,
                escalated,
            ),
            Err(KernelError::CapabilityEscalation {
                role: ProcessRole::Renderer,
            })
        );
    }

    #[test]
    fn stale_process_epoch_is_rejected_after_restart() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let renderer = registry
            .launch(
                registry.kernel(),
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        let restarted = registry
            .restart(registry.kernel(), renderer)
            .expect("kernel restarts renderer");
        assert_eq!(restarted.id(), renderer.id());
        assert_ne!(restarted.epoch(), renderer.epoch());
        assert!(matches!(
            registry.policy(renderer),
            Err(KernelError::StaleProcess { .. })
        ));
    }

    #[test]
    fn generated_route_and_capability_are_enforced() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let renderer = registry
            .launch(
                registry.kernel(),
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
            )
            .expect("kernel launches renderer");
        let network = registry
            .launch(
                registry.kernel(),
                ProcessId::new(3).expect("valid network id"),
                ProcessRole::Network,
            )
            .expect("kernel launches network");
        let invalid = envelope(MessageKind::NavigationIntent, renderer, network, 1, 1);
        assert_eq!(
            registry.authorize(&invalid),
            Err(KernelError::RouteDenied {
                kind: MessageKind::NavigationIntent,
                sender: ProcessRole::Renderer,
                receiver: ProcessRole::Network,
            })
        );
    }

    #[test]
    fn attenuated_process_cannot_use_removed_capability() {
        let mut registry = ProcessRegistry::new(ProcessId::new(1).expect("valid kernel id"));
        let capabilities =
            CapabilitySet::for_role(ProcessRole::Renderer).without(Capability::RequestNavigation);
        let renderer = registry
            .launch_with_capabilities(
                registry.kernel(),
                ProcessId::new(2).expect("valid renderer id"),
                ProcessRole::Renderer,
                capabilities,
            )
            .expect("attenuated launch is valid");
        let message = envelope(
            MessageKind::NavigationIntent,
            renderer,
            registry.kernel(),
            1,
            1,
        );
        assert_eq!(
            registry.authorize(&message),
            Err(KernelError::MissingCapability {
                role: ProcessRole::Renderer,
                capability: Capability::RequestNavigation,
            })
        );
    }

    #[test]
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
        let mismatched = envelope(MessageKind::NavigationIntent, other_renderer, kernel, 1, 2);
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
