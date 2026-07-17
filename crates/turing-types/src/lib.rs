// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use core::fmt;
use core::num::NonZeroU64;

/// Error returned when a typed identity is constructed from zero.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ZeroIdError {
    kind: &'static str,
}

impl ZeroIdError {
    /// Returns the identity kind that rejected zero.
    #[must_use]
    pub const fn kind(self) -> &'static str {
        self.kind
    }
}

impl fmt::Display for ZeroIdError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{} must be non-zero", self.kind)
    }
}

impl std::error::Error for ZeroIdError {}

macro_rules! define_id {
    ($name:ident, $kind:literal) => {
        #[doc = concat!("Stable non-zero identity for ", $kind, ".")]
        #[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
        pub struct $name(NonZeroU64);

        impl $name {
            #[doc = concat!("Creates a ", $kind, " identity.")]
            pub const fn new(value: u64) -> Result<Self, ZeroIdError> {
                match NonZeroU64::new(value) {
                    Some(value) => Ok(Self(value)),
                    None => Err(ZeroIdError { kind: $kind }),
                }
            }

            #[doc = concat!("Returns the raw non-zero ", $kind, " identity.")]
            #[must_use]
            pub const fn get(self) -> u64 {
                self.0.get()
            }
        }

        impl fmt::Display for $name {
            fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
                self.0.fmt(formatter)
            }
        }
    };
}

define_id!(ProcessId, "process");
define_id!(PrincipalId, "principal");
define_id!(WindowId, "window");
define_id!(ProfileId, "profile");
define_id!(SpaceId, "space");
define_id!(TabId, "tab");
define_id!(ViewId, "view");
define_id!(DocumentEpoch, "document epoch");
define_id!(OperationId, "operation");
define_id!(SequenceNumber, "sequence number");

#[cfg(test)]
mod tests {
    use super::{ProcessId, ZeroIdError};

    #[test]
    fn typed_ids_reject_zero() {
        assert_eq!(ProcessId::new(0), Err(ZeroIdError { kind: "process" }));
    }

    #[test]
    fn typed_ids_round_trip_non_zero_values() {
        let id = ProcessId::new(42).expect("42 is non-zero");
        assert_eq!(id.get(), 42);
        assert_eq!(id.to_string(), "42");
    }
}
