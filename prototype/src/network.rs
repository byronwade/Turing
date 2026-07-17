// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct ProfileId(String);

impl ProfileId {
    pub fn new(value: impl Into<String>) -> Result<Self, ContextError> {
        let value = value.into();
        if value.is_empty() || value.len() > 128 {
            return Err(ContextError::ProfileId);
        }
        Ok(Self(value))
    }

    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct DocumentEpoch(u64);

impl DocumentEpoch {
    pub fn new(value: u64) -> Result<Self, ContextError> {
        if value == 0 {
            return Err(ContextError::DocumentEpoch);
        }
        Ok(Self(value))
    }

    #[must_use]
    pub const fn get(self) -> u64 {
        self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Origin(String);

impl Origin {
    pub fn parse_ascii(value: impl Into<String>) -> Result<Self, ContextError> {
        let value = value.into();
        if value.len() > 4096
            || !(value.starts_with("https://") || value.starts_with("http://") || value == "opaque")
        {
            return Err(ContextError::Origin);
        }
        Ok(Self(value))
    }

    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct TopLevelSite(String);

impl TopLevelSite {
    pub fn parse_ascii(value: impl Into<String>) -> Result<Self, ContextError> {
        let value = value.into();
        if value.len() > 4096 || !(value.starts_with("https://") || value.starts_with("http://")) {
            return Err(ContextError::TopLevelSite);
        }
        Ok(Self(value))
    }

    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[expect(
    dead_code,
    reason = "the reference model preserves all Fetch credential modes beyond the smoke path"
)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CredentialMode {
    Omit,
    SameOrigin,
    Include,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RequestContext {
    pub profile: ProfileId,
    pub document_epoch: DocumentEpoch,
    pub requesting_origin: Origin,
    pub top_level_site: TopLevelSite,
    pub destination_url: String,
    pub credentials: CredentialMode,
    pub network_partition: String,
}

impl RequestContext {
    pub fn new(
        profile: ProfileId,
        document_epoch: DocumentEpoch,
        requesting_origin: Origin,
        top_level_site: TopLevelSite,
        destination_url: impl Into<String>,
        credentials: CredentialMode,
        network_partition: impl Into<String>,
    ) -> Result<Self, ContextError> {
        let destination_url = destination_url.into();
        if destination_url.len() > 8192
            || !(destination_url.starts_with("https://") || destination_url.starts_with("http://"))
        {
            return Err(ContextError::Destination);
        }

        let network_partition = network_partition.into();
        if network_partition.is_empty() || network_partition.len() > 512 {
            return Err(ContextError::Partition);
        }

        Ok(Self {
            profile,
            document_epoch,
            requesting_origin,
            top_level_site,
            destination_url,
            credentials,
            network_partition,
        })
    }

    #[expect(
        dead_code,
        reason = "the stale-epoch predicate is exercised by tests and future navigation experiments"
    )]
    #[must_use]
    pub fn is_current_for(&self, epoch: DocumentEpoch) -> bool {
        self.document_epoch == epoch
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ContextError {
    ProfileId,
    DocumentEpoch,
    Origin,
    TopLevelSite,
    Destination,
    Partition,
}

impl fmt::Display for ContextError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::ProfileId => "invalid profile identifier",
            Self::DocumentEpoch => "document epoch must be nonzero",
            Self::Origin => "invalid origin",
            Self::TopLevelSite => "invalid top-level site",
            Self::Destination => "invalid network destination",
            Self::Partition => "invalid network partition",
        };
        formatter.write_str(message)
    }
}

impl std::error::Error for ContextError {}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_context() -> RequestContext {
        RequestContext::new(
            ProfileId::new("default").unwrap(),
            DocumentEpoch::new(7).unwrap(),
            Origin::parse_ascii("https://app.example").unwrap(),
            TopLevelSite::parse_ascii("https://example").unwrap(),
            "https://api.example/data",
            CredentialMode::SameOrigin,
            "default|https://example",
        )
        .unwrap()
    }

    #[test]
    fn request_identity_is_explicit() {
        let context = sample_context();
        assert_eq!(context.profile.as_str(), "default");
        assert_eq!(context.requesting_origin.as_str(), "https://app.example");
        assert_eq!(context.top_level_site.as_str(), "https://example");
    }

    #[test]
    fn stale_document_context_is_detected() {
        let context = sample_context();
        assert!(context.is_current_for(DocumentEpoch::new(7).unwrap()));
        assert!(!context.is_current_for(DocumentEpoch::new(8).unwrap()));
    }

    #[test]
    fn local_file_destination_is_not_accepted_by_default() {
        let result = RequestContext::new(
            ProfileId::new("default").unwrap(),
            DocumentEpoch::new(1).unwrap(),
            Origin::parse_ascii("https://example").unwrap(),
            TopLevelSite::parse_ascii("https://example").unwrap(),
            "file:///etc/passwd",
            CredentialMode::Omit,
            "default|https://example",
        );
        assert_eq!(result, Err(ContextError::Destination));
    }
}
