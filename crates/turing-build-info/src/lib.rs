// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

/// Maturity label embedded into build identity.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Maturity {
    /// Architecture or subsystem experiment; not a browser release.
    Research,
    /// Early developer-only preview.
    DeveloperPreview,
    /// Beta release with explicit support limits.
    Beta,
    /// Stable release after all production gates pass.
    Stable,
}

/// Immutable build identity exposed by Turing binaries.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct BuildIdentity {
    /// Cargo package version.
    pub version: &'static str,
    /// Optional source commit injected by the release build.
    pub source_commit: Option<&'static str>,
    /// Build maturity.
    pub maturity: Maturity,
}

impl BuildIdentity {
    /// Returns the identity of the current M0 shell laboratory.
    #[must_use]
    pub const fn current() -> Self {
        Self {
            version: env!("CARGO_PKG_VERSION"),
            source_commit: option_env!("TURING_GIT_COMMIT"),
            maturity: Maturity::Research,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{BuildIdentity, Maturity};

    #[test]
    fn current_build_is_research_only() {
        let identity = BuildIdentity::current();
        assert_eq!(identity.maturity, Maturity::Research);
        assert!(!identity.version.is_empty());
    }
}
