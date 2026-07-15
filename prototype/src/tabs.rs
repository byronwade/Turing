// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use std::collections::BTreeSet;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum TabState {
    Active,
    Background,
    Throttled,
    Frozen,
    Serialized,
    Discarded,
    Crashed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ProtectionReason {
    AudibleMedia,
    Capture,
    RealTimeCall,
    Transfer,
    UnsavedWork,
    DeviceSession,
    DevToolsAttached,
    UserKeepActive,
    EnterprisePolicy,
    AgentConfirmation,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TabLifecycle {
    state: TabState,
    protections: BTreeSet<ProtectionReason>,
    transition_epoch: u64,
}

impl TabLifecycle {
    #[must_use]
    pub fn new() -> Self {
        Self {
            state: TabState::Active,
            protections: BTreeSet::new(),
            transition_epoch: 1,
        }
    }

    #[must_use]
    pub const fn state(&self) -> TabState {
        self.state
    }

    #[must_use]
    pub const fn transition_epoch(&self) -> u64 {
        self.transition_epoch
    }

    pub fn protect(&mut self, reason: ProtectionReason) {
        self.protections.insert(reason);
    }

    pub fn remove_protection(&mut self, reason: ProtectionReason) {
        self.protections.remove(&reason);
    }

    #[must_use]
    pub fn protections(&self) -> impl Iterator<Item = ProtectionReason> + '_ {
        self.protections.iter().copied()
    }

    pub fn transition(&mut self, next: TabState) -> Result<(), LifecycleError> {
        if next == self.state {
            return Ok(());
        }

        if self.state == TabState::Crashed && next != TabState::Active {
            return Err(LifecycleError::IllegalTransition {
                from: self.state,
                to: next,
            });
        }

        if matches!(next, TabState::Frozen | TabState::Serialized | TabState::Discarded)
            && !self.protections.is_empty()
        {
            return Err(LifecycleError::Protected {
                requested: next,
                reasons: self.protections.iter().copied().collect(),
            });
        }

        if !is_legal_edge(self.state, next) {
            return Err(LifecycleError::IllegalTransition {
                from: self.state,
                to: next,
            });
        }

        self.state = next;
        self.transition_epoch = self
            .transition_epoch
            .checked_add(1)
            .ok_or(LifecycleError::EpochOverflow)?;
        Ok(())
    }
}

impl Default for TabLifecycle {
    fn default() -> Self {
        Self::new()
    }
}

const fn is_legal_edge(from: TabState, to: TabState) -> bool {
    use TabState::{Active, Background, Crashed, Discarded, Frozen, Serialized, Throttled};

    matches!(
        (from, to),
        (Active, Background)
            | (Active, Crashed)
            | (Background, Active)
            | (Background, Throttled)
            | (Background, Frozen)
            | (Background, Crashed)
            | (Throttled, Active)
            | (Throttled, Background)
            | (Throttled, Frozen)
            | (Throttled, Crashed)
            | (Frozen, Active)
            | (Frozen, Background)
            | (Frozen, Serialized)
            | (Frozen, Discarded)
            | (Frozen, Crashed)
            | (Serialized, Active)
            | (Serialized, Discarded)
            | (Serialized, Crashed)
            | (Discarded, Active)
            | (Crashed, Active)
    )
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LifecycleError {
    IllegalTransition { from: TabState, to: TabState },
    Protected {
        requested: TabState,
        reasons: Vec<ProtectionReason>,
    },
    EpochOverflow,
}

impl fmt::Display for LifecycleError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::IllegalTransition { from, to } => {
                write!(formatter, "illegal tab transition from {from:?} to {to:?}")
            }
            Self::Protected { requested, reasons } => write!(
                formatter,
                "tab cannot enter {requested:?}; protection reasons: {reasons:?}"
            ),
            Self::EpochOverflow => write!(formatter, "tab transition epoch overflow"),
        }
    }
}

impl std::error::Error for LifecycleError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn normal_pressure_path_is_explicit() {
        let mut tab = TabLifecycle::new();
        tab.transition(TabState::Background).unwrap();
        tab.transition(TabState::Throttled).unwrap();
        tab.transition(TabState::Frozen).unwrap();
        tab.transition(TabState::Serialized).unwrap();
        tab.transition(TabState::Discarded).unwrap();
        assert_eq!(tab.state(), TabState::Discarded);
    }

    #[test]
    fn unsaved_work_blocks_freeze_and_discard() {
        let mut tab = TabLifecycle::new();
        tab.transition(TabState::Background).unwrap();
        tab.protect(ProtectionReason::UnsavedWork);

        let result = tab.transition(TabState::Frozen);
        assert!(matches!(
            result,
            Err(LifecycleError::Protected {
                requested: TabState::Frozen,
                ..
            })
        ));
        assert_eq!(tab.state(), TabState::Background);
    }

    #[test]
    fn crash_recovery_is_not_called_a_normal_lifecycle_transition() {
        let mut tab = TabLifecycle::new();
        tab.transition(TabState::Crashed).unwrap();
        assert!(tab.transition(TabState::Background).is_err());
        tab.transition(TabState::Active).unwrap();
    }
}
