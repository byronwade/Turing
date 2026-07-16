// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use std::collections::BTreeSet;

use crate::network::{DocumentEpoch, Origin, ProfileId};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum RiskClass {
    Observe = 0,
    ReversibleLocal = 1,
    ExternalLowImpact = 2,
    Consequential = 3,
    HighRisk = 4,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ActionKind {
    Observe,
    Navigate,
    OrganizeTabs,
    EditText,
    SubmitSearch,
    Download,
    Upload,
    SendOrPublish,
    Purchase,
    CredentialUse,
    PermissionGrant,
    DestructiveChange,
    DevToolsEvaluate,
}

impl ActionKind {
    #[must_use]
    pub const fn risk(self) -> RiskClass {
        match self {
            Self::Observe => RiskClass::Observe,
            Self::Navigate | Self::OrganizeTabs | Self::EditText => RiskClass::ReversibleLocal,
            Self::SubmitSearch | Self::Download => RiskClass::ExternalLowImpact,
            Self::Upload | Self::SendOrPublish | Self::DevToolsEvaluate => RiskClass::Consequential,
            Self::Purchase
            | Self::CredentialUse
            | Self::PermissionGrant
            | Self::DestructiveChange => RiskClass::HighRisk,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AgentGrant {
    pub principal_id: String,
    pub profile: ProfileId,
    pub allowed_origins: BTreeSet<Origin>,
    pub allowed_actions: BTreeSet<ActionKind>,
    pub expires_at_unix_seconds: u64,
    pub maximum_actions: u32,
}

impl AgentGrant {
    #[must_use]
    pub fn allows_origin(&self, origin: &Origin) -> bool {
        self.allowed_origins.contains(origin)
    }

    #[must_use]
    pub fn allows_action(&self, action: ActionKind) -> bool {
        self.allowed_actions.contains(&action)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AgentAction {
    pub principal_id: String,
    pub profile: ProfileId,
    pub origin: Origin,
    pub document_epoch: DocumentEpoch,
    pub kind: ActionKind,
    pub prior_action_count: u32,
    pub confirmed: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    Approved { risk: RiskClass },
    Denied(DenyReason),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DenyReason {
    PrincipalMismatch,
    ProfileMismatch,
    OriginNotGranted,
    ActionNotGranted,
    GrantExpired,
    ActionQuotaExhausted,
    StaleDocument,
    ConfirmationRequired,
}

#[must_use]
pub fn authorize(
    now_unix_seconds: u64,
    current_document_epoch: DocumentEpoch,
    grant: &AgentGrant,
    action: &AgentAction,
) -> Decision {
    if action.principal_id != grant.principal_id {
        return Decision::Denied(DenyReason::PrincipalMismatch);
    }
    if action.profile != grant.profile {
        return Decision::Denied(DenyReason::ProfileMismatch);
    }
    if !grant.allows_origin(&action.origin) {
        return Decision::Denied(DenyReason::OriginNotGranted);
    }
    if !grant.allows_action(action.kind) {
        return Decision::Denied(DenyReason::ActionNotGranted);
    }
    if now_unix_seconds > grant.expires_at_unix_seconds {
        return Decision::Denied(DenyReason::GrantExpired);
    }
    if action.prior_action_count >= grant.maximum_actions {
        return Decision::Denied(DenyReason::ActionQuotaExhausted);
    }
    if action.document_epoch != current_document_epoch {
        return Decision::Denied(DenyReason::StaleDocument);
    }

    let risk = action.kind.risk();
    if risk >= RiskClass::Consequential && !action.confirmed {
        return Decision::Denied(DenyReason::ConfirmationRequired);
    }

    Decision::Approved { risk }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn origin(value: &str) -> Origin {
        Origin::parse_ascii(value).unwrap()
    }

    fn profile() -> ProfileId {
        ProfileId::new("personal").unwrap()
    }

    fn grant() -> AgentGrant {
        AgentGrant {
            principal_id: "agent.local.dev".to_string(),
            profile: profile(),
            allowed_origins: [origin("https://example.test")].into_iter().collect(),
            allowed_actions: [
                ActionKind::Observe,
                ActionKind::Navigate,
                ActionKind::Upload,
            ]
            .into_iter()
            .collect(),
            expires_at_unix_seconds: 2_000,
            maximum_actions: 10,
        }
    }

    fn action(kind: ActionKind) -> AgentAction {
        AgentAction {
            principal_id: "agent.local.dev".to_string(),
            profile: profile(),
            origin: origin("https://example.test"),
            document_epoch: DocumentEpoch::new(5).unwrap(),
            kind,
            prior_action_count: 0,
            confirmed: false,
        }
    }

    #[test]
    fn observation_can_be_approved_without_confirmation() {
        assert_eq!(
            authorize(
                1_000,
                DocumentEpoch::new(5).unwrap(),
                &grant(),
                &action(ActionKind::Observe)
            ),
            Decision::Approved {
                risk: RiskClass::Observe
            }
        );
    }

    #[test]
    fn consequential_action_needs_confirmation() {
        assert_eq!(
            authorize(
                1_000,
                DocumentEpoch::new(5).unwrap(),
                &grant(),
                &action(ActionKind::Upload)
            ),
            Decision::Denied(DenyReason::ConfirmationRequired)
        );
    }

    #[test]
    fn confirmation_does_not_override_a_stale_document() {
        let mut stale = action(ActionKind::Upload);
        stale.confirmed = true;
        assert_eq!(
            authorize(1_000, DocumentEpoch::new(6).unwrap(), &grant(), &stale),
            Decision::Denied(DenyReason::StaleDocument)
        );
    }

    #[test]
    fn page_origin_cannot_expand_a_grant() {
        let mut injected = action(ActionKind::Navigate);
        injected.origin = origin("https://attacker.test");
        assert_eq!(
            authorize(1_000, DocumentEpoch::new(5).unwrap(), &grant(), &injected),
            Decision::Denied(DenyReason::OriginNotGranted)
        );
    }

    #[test]
    fn expired_grant_is_rejected() {
        assert_eq!(
            authorize(
                2_001,
                DocumentEpoch::new(5).unwrap(),
                &grant(),
                &action(ActionKind::Navigate)
            ),
            Decision::Denied(DenyReason::GrantExpired)
        );
    }
}
