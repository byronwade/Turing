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

            #[doc = concat!("Returns the next ", $kind, " identity when it does not overflow.")]
            #[must_use]
            pub fn checked_next(self) -> Option<Self> {
                self.get()
                    .checked_add(1)
                    .and_then(NonZeroU64::new)
                    .map(Self)
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
define_id!(ProcessEpoch, "process epoch");
define_id!(PrincipalId, "principal");
define_id!(WindowId, "window");
define_id!(ProfileId, "profile");
define_id!(SpaceId, "space");
define_id!(TabId, "tab");
define_id!(ViewId, "view");
define_id!(SurfaceId, "surface");
define_id!(DocumentEpoch, "document epoch");
define_id!(DeviceGeneration, "device generation");
define_id!(OperationId, "operation");
define_id!(ChannelId, "channel");
define_id!(SequenceNumber, "sequence number");

/// Restart-safe identity for one operating-system process instance.
///
/// A numeric process ID may be reused only with a strictly newer epoch. IPC
/// authorization validates the complete pair so messages from an exited
/// process cannot target a replacement process accidentally.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ProcessIdentity {
    id: ProcessId,
    epoch: ProcessEpoch,
}

impl ProcessIdentity {
    /// Creates a process identity from a stable ID and restart epoch.
    #[must_use]
    pub const fn new(id: ProcessId, epoch: ProcessEpoch) -> Self {
        Self { id, epoch }
    }

    /// Returns the stable process ID.
    #[must_use]
    pub const fn id(self) -> ProcessId {
        self.id
    }

    /// Returns the restart epoch.
    #[must_use]
    pub const fn epoch(self) -> ProcessEpoch {
        self.epoch
    }
}

impl fmt::Display for ProcessIdentity {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}@{}", self.id, self.epoch)
    }
}

#[cfg(test)]
mod tests {
    use super::{
        DeviceGeneration, ProcessEpoch, ProcessId, ProcessIdentity, SequenceNumber, SurfaceId,
        ZeroIdError,
    };

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

    #[test]
    fn surface_generations_are_typed_non_zero_ids() {
        let surface = SurfaceId::new(4).expect("valid surface id");
        let device = DeviceGeneration::new(2).expect("valid device generation");
        assert_eq!(surface.get(), 4);
        assert_eq!(device.get(), 2);
    }

    #[test]
    fn typed_ids_increment_without_wrapping() {
        let sequence = SequenceNumber::new(7).expect("valid sequence");
        assert_eq!(sequence.checked_next().expect("no overflow").get(), 8);
        let maximum = SequenceNumber::new(u64::MAX).expect("maximum is non-zero");
        assert_eq!(maximum.checked_next(), None);
    }

    #[test]
    fn process_identity_includes_restart_epoch() {
        let identity = ProcessIdentity::new(
            ProcessId::new(9).expect("valid process"),
            ProcessEpoch::new(3).expect("valid epoch"),
        );
        assert_eq!(identity.to_string(), "9@3");
    }
}
