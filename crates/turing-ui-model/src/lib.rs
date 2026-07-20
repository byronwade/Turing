// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use std::collections::BTreeSet;
use std::fmt;

use turing_types::{ProfileId, SpaceId, TabId, ViewId, WindowId};

/// User-visible lifecycle state of a tab.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum TabLifecycle {
    /// Foreground interactive tab.
    Active,
    /// Background live tab.
    Background,
    /// Execution suspended while restorable state is retained.
    Frozen,
    /// Reload or serialized restoration is required.
    Discarded,
    /// Restoration is in progress.
    Restoring,
}

/// Presentation summary for one tab.
///
/// This intentionally contains no toolkit types, page pointers, credentials, or
/// mutable renderer state.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct TabSummary {
    /// Stable tab identity.
    pub id: TabId,
    /// Page view identity.
    pub view: ViewId,
    /// Display title supplied through trusted sanitization.
    pub title: String,
    /// Display URL supplied through trusted URL formatting.
    pub display_url: String,
    /// Lifecycle state.
    pub lifecycle: TabLifecycle,
    /// Whether unsaved work currently protects this tab from discard.
    pub protects_unsaved_work: bool,
}

/// Immutable presentation state for a browser window.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ShellSnapshot {
    /// Monotonic presentation version.
    pub version: u64,
    /// Window identity.
    pub window: WindowId,
    /// Profile identity.
    pub profile: ProfileId,
    /// Active project Space.
    pub space: SpaceId,
    /// Active tab, when any.
    pub active_tab: Option<TabId>,
    /// Tabs visible to the window.
    pub tabs: Vec<TabSummary>,
}

/// Validation failure for a shell snapshot.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum SnapshotError {
    /// Snapshot versions begin at one.
    ZeroVersion,
    /// Duplicate tab identity.
    DuplicateTab(TabId),
    /// Active tab does not exist in the snapshot.
    MissingActiveTab(TabId),
}

impl fmt::Display for SnapshotError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroVersion => write!(formatter, "shell snapshot version must be non-zero"),
            Self::DuplicateTab(tab) => write!(formatter, "duplicate tab identity {tab}"),
            Self::MissingActiveTab(tab) => write!(formatter, "active tab {tab} is not present"),
        }
    }
}

impl std::error::Error for SnapshotError {}

impl ShellSnapshot {
    /// Validates identity and version invariants.
    pub fn validate(&self) -> Result<(), SnapshotError> {
        if self.version == 0 {
            return Err(SnapshotError::ZeroVersion);
        }

        let mut ids = BTreeSet::new();
        for tab in &self.tabs {
            if !ids.insert(tab.id) {
                return Err(SnapshotError::DuplicateTab(tab.id));
            }
        }

        if let Some(active_tab) = self.active_tab
            && !ids.contains(&active_tab)
        {
            return Err(SnapshotError::MissingActiveTab(active_tab));
        }

        Ok(())
    }
}

/// Typed intent emitted by browser chrome.
///
/// The browser kernel or owning service revalidates every command before any
/// privileged or persistent effect occurs.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ShellCommand {
    /// Activate one tab.
    ActivateTab { tab: TabId },
    /// Request closing one tab.
    CloseTab { tab: TabId },
    /// Request navigation in one page view.
    Navigate { view: ViewId, input: String },
    /// Freeze one tab if current protection and policy permit.
    FreezeTab { tab: TabId },
    /// Restore one discarded tab.
    RestoreTab { tab: TabId },
    /// Switch project Space.
    ActivateSpace { space: SpaceId },
    /// Open a new tab. The owning service chooses identifiers and initial
    /// content; chrome only expresses the intent.
    NewTab,
    /// Reload one tab's current content.
    Reload { tab: TabId },
    /// Open the command field focused for typed input, in the context of one
    /// tab when the chrome knows it (the Nova design opens it from the active
    /// tab, which doubles as the address field).
    OpenCommandField { tab: Option<TabId> },
}

#[cfg(test)]
mod tests {
    use super::{ShellSnapshot, SnapshotError, TabLifecycle, TabSummary};
    use turing_types::{ProfileId, SpaceId, TabId, ViewId, WindowId};

    fn sample_tab(id: u64) -> TabSummary {
        TabSummary {
            id: TabId::new(id).expect("valid tab id"),
            view: ViewId::new(id).expect("valid view id"),
            title: format!("Tab {id}"),
            display_url: "about:blank".to_owned(),
            lifecycle: TabLifecycle::Active,
            protects_unsaved_work: false,
        }
    }

    fn sample_snapshot() -> ShellSnapshot {
        ShellSnapshot {
            version: 1,
            window: WindowId::new(1).expect("valid window id"),
            profile: ProfileId::new(1).expect("valid profile id"),
            space: SpaceId::new(1).expect("valid space id"),
            active_tab: Some(TabId::new(1).expect("valid tab id")),
            tabs: vec![sample_tab(1)],
        }
    }

    #[test]
    fn accepts_consistent_snapshot() {
        assert_eq!(sample_snapshot().validate(), Ok(()));
    }

    #[test]
    fn rejects_missing_active_tab() {
        let mut snapshot = sample_snapshot();
        snapshot.active_tab = Some(TabId::new(2).expect("valid tab id"));

        assert_eq!(
            snapshot.validate(),
            Err(SnapshotError::MissingActiveTab(
                TabId::new(2).expect("valid tab id")
            ))
        );
    }

    #[test]
    fn rejects_duplicate_tabs() {
        let mut snapshot = sample_snapshot();
        snapshot.tabs.push(sample_tab(1));

        assert_eq!(
            snapshot.validate(),
            Err(SnapshotError::DuplicateTab(
                TabId::new(1).expect("valid tab id")
            ))
        );
    }
}
