// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use std::collections::BTreeSet;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ProcessRole {
    BrowserKernel,
    Renderer,
    Network,
    Storage,
    Gpu,
    MediaUtility,
    ExtensionHost,
    DevTools,
    AgentHost,
    Updater,
    CrashHandler,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Capability {
    LaunchProcesses,
    AssignIdentity,
    CommitNavigation,
    OpenNetworkSockets,
    AccessProfileStorage,
    AccessGraphicsDevice,
    AccessTaskScopedInput,
    UseExtensionApi,
    InspectAttachedTarget,
    RequestModelInference,
    VerifyAndInstallUpdate,
    CaptureCrash,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CapabilitySet {
    role: ProcessRole,
    allowed: BTreeSet<Capability>,
}

impl CapabilitySet {
    #[must_use]
    pub fn for_role(role: ProcessRole) -> Self {
        let allowed = match role {
            ProcessRole::BrowserKernel => [
                Capability::LaunchProcesses,
                Capability::AssignIdentity,
                Capability::CommitNavigation,
            ]
            .into_iter()
            .collect(),
            ProcessRole::Renderer => BTreeSet::new(),
            ProcessRole::Network => [Capability::OpenNetworkSockets].into_iter().collect(),
            ProcessRole::Storage => [Capability::AccessProfileStorage].into_iter().collect(),
            ProcessRole::Gpu => [Capability::AccessGraphicsDevice].into_iter().collect(),
            ProcessRole::MediaUtility => [Capability::AccessTaskScopedInput].into_iter().collect(),
            ProcessRole::ExtensionHost => [Capability::UseExtensionApi].into_iter().collect(),
            ProcessRole::DevTools => [Capability::InspectAttachedTarget].into_iter().collect(),
            ProcessRole::AgentHost => [Capability::RequestModelInference].into_iter().collect(),
            ProcessRole::Updater => [Capability::VerifyAndInstallUpdate].into_iter().collect(),
            ProcessRole::CrashHandler => [Capability::CaptureCrash].into_iter().collect(),
        };

        Self { role, allowed }
    }

    #[must_use]
    pub const fn role(&self) -> ProcessRole {
        self.role
    }

    #[must_use]
    pub fn permits(&self, capability: Capability) -> bool {
        self.allowed.contains(&capability)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MessageEnvelope<T> {
    pub sequence: u64,
    pub sender: ProcessRole,
    pub receiver: ProcessRole,
    pub encoded_len: usize,
    pub payload: T,
}

impl<T> MessageEnvelope<T> {
    pub fn bounded(
        sequence: u64,
        sender: ProcessRole,
        receiver: ProcessRole,
        encoded_len: usize,
        maximum_len: usize,
        payload: T,
    ) -> Result<Self, MessageError> {
        if maximum_len == 0 {
            return Err(MessageError::InvalidMaximum);
        }
        if encoded_len > maximum_len {
            return Err(MessageError::TooLarge {
                encoded_len,
                maximum_len,
            });
        }

        Ok(Self {
            sequence,
            sender,
            receiver,
            encoded_len,
            payload,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MessageError {
    InvalidMaximum,
    TooLarge {
        encoded_len: usize,
        maximum_len: usize,
    },
}

impl fmt::Display for MessageError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidMaximum => write!(formatter, "message maximum must be greater than zero"),
            Self::TooLarge {
                encoded_len,
                maximum_len,
            } => write!(
                formatter,
                "encoded message length {encoded_len} exceeds maximum {maximum_len}"
            ),
        }
    }
}

impl std::error::Error for MessageError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn renderer_has_no_ambient_capabilities() {
        let renderer = CapabilitySet::for_role(ProcessRole::Renderer);
        assert!(!renderer.permits(Capability::OpenNetworkSockets));
        assert!(!renderer.permits(Capability::AccessProfileStorage));
        assert!(!renderer.permits(Capability::VerifyAndInstallUpdate));
    }

    #[test]
    fn network_role_is_narrow() {
        let network = CapabilitySet::for_role(ProcessRole::Network);
        assert!(network.permits(Capability::OpenNetworkSockets));
        assert!(!network.permits(Capability::AccessProfileStorage));
        assert!(!network.permits(Capability::AssignIdentity));
    }

    #[test]
    fn message_size_is_enforced_before_acceptance() {
        let result = MessageEnvelope::bounded(
            1,
            ProcessRole::Renderer,
            ProcessRole::BrowserKernel,
            65,
            64,
            "payload",
        );
        assert_eq!(
            result,
            Err(MessageError::TooLarge {
                encoded_len: 65,
                maximum_len: 64
            })
        );
    }
}
