// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use turing_types::ProcessId;

/// Process roles recognized by the M0 kernel contract.
#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub enum ProcessRole {
    /// Privileged browser policy and process broker.
    BrowserKernel,
    /// Untrusted web renderer.
    Renderer,
    /// Network service.
    Network,
    /// Persistent storage service.
    Storage,
    /// GPU command validation and presentation.
    Gpu,
    /// Hostile media, image, font, or document decoder.
    Decoder,
    /// Turing Plug-in host.
    Plugin,
    /// Developer tools host.
    DevTools,
    /// AI or automation agent host.
    Agent,
    /// Update and package verification service.
    Updater,
    /// Crash collection service.
    CrashReporter,
}

/// Explicit capabilities granted by the browser kernel.
#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
#[repr(u8)]
pub enum Capability {
    /// Connect to external network destinations.
    OpenNetworkSockets = 0,
    /// Read arbitrary filesystem paths.
    ReadArbitraryFiles = 1,
    /// Write arbitrary filesystem paths.
    WriteArbitraryFiles = 2,
    /// Access profile-scoped storage through a broker.
    UseProfileStorage = 3,
    /// Submit validated GPU work.
    SubmitGpuWork = 4,
    /// Decode bounded hostile inputs.
    DecodeHostileInput = 5,
    /// Emit browser-facing diagnostics.
    EmitDiagnostics = 6,
    /// Request browser navigation through a typed broker.
    RequestNavigation = 7,
    /// Verify and stage signed updates.
    StageVerifiedUpdate = 8,
}

/// Compact set of explicit process capabilities.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct CapabilitySet(u128);

impl CapabilitySet {
    /// Empty capability set.
    pub const EMPTY: Self = Self(0);

    /// Inserts one capability.
    #[must_use]
    pub const fn with(self, capability: Capability) -> Self {
        Self(self.0 | (1_u128 << capability as u8))
    }

    /// Returns whether the capability is present.
    #[must_use]
    pub const fn contains(self, capability: Capability) -> bool {
        self.0 & (1_u128 << capability as u8) != 0
    }

    /// Returns the default capability set for a process role.
    #[must_use]
    pub const fn for_role(role: ProcessRole) -> Self {
        match role {
            ProcessRole::BrowserKernel => Self::EMPTY
                .with(Capability::ReadArbitraryFiles)
                .with(Capability::WriteArbitraryFiles)
                .with(Capability::EmitDiagnostics),
            ProcessRole::Renderer => Self::EMPTY
                .with(Capability::RequestNavigation)
                .with(Capability::EmitDiagnostics),
            ProcessRole::Network => Self::EMPTY
                .with(Capability::OpenNetworkSockets)
                .with(Capability::EmitDiagnostics),
            ProcessRole::Storage => Self::EMPTY
                .with(Capability::UseProfileStorage)
                .with(Capability::EmitDiagnostics),
            ProcessRole::Gpu => Self::EMPTY
                .with(Capability::SubmitGpuWork)
                .with(Capability::EmitDiagnostics),
            ProcessRole::Decoder => Self::EMPTY
                .with(Capability::DecodeHostileInput)
                .with(Capability::EmitDiagnostics),
            ProcessRole::Plugin | ProcessRole::DevTools | ProcessRole::Agent => {
                Self::EMPTY.with(Capability::EmitDiagnostics)
            }
            ProcessRole::Updater => Self::EMPTY
                .with(Capability::StageVerifiedUpdate)
                .with(Capability::EmitDiagnostics),
            ProcessRole::CrashReporter => Self::EMPTY.with(Capability::EmitDiagnostics),
        }
    }
}

/// One process identity, role, and capability assignment.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ProcessPolicy {
    /// Stable process identity.
    pub id: ProcessId,
    /// Assigned process role.
    pub role: ProcessRole,
    /// Explicit capabilities.
    pub capabilities: CapabilitySet,
}

impl ProcessPolicy {
    /// Creates the default policy for one process role.
    #[must_use]
    pub const fn for_role(id: ProcessId, role: ProcessRole) -> Self {
        Self {
            id,
            role,
            capabilities: CapabilitySet::for_role(role),
        }
    }

    /// Returns whether this process may exercise a capability.
    #[must_use]
    pub const fn allows(self, capability: Capability) -> bool {
        self.capabilities.contains(capability)
    }
}

#[cfg(test)]
mod tests {
    use super::{Capability, ProcessPolicy, ProcessRole};
    use turing_types::ProcessId;

    #[test]
    fn renderers_have_no_ambient_network_or_file_access() {
        let renderer = ProcessPolicy::for_role(
            ProcessId::new(1).expect("valid process id"),
            ProcessRole::Renderer,
        );

        assert!(!renderer.allows(Capability::OpenNetworkSockets));
        assert!(!renderer.allows(Capability::ReadArbitraryFiles));
        assert!(!renderer.allows(Capability::WriteArbitraryFiles));
        assert!(renderer.allows(Capability::RequestNavigation));
    }

    #[test]
    fn network_process_has_network_but_not_profile_storage() {
        let network = ProcessPolicy::for_role(
            ProcessId::new(2).expect("valid process id"),
            ProcessRole::Network,
        );

        assert!(network.allows(Capability::OpenNetworkSockets));
        assert!(!network.allows(Capability::UseProfileStorage));
    }

    #[test]
    fn agent_has_no_ambient_browser_authority() {
        let agent = ProcessPolicy::for_role(
            ProcessId::new(3).expect("valid process id"),
            ProcessRole::Agent,
        );

        assert!(!agent.allows(Capability::OpenNetworkSockets));
        assert!(!agent.allows(Capability::UseProfileStorage));
        assert!(!agent.allows(Capability::RequestNavigation));
    }
}
