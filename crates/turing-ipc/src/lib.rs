// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

use core::fmt;

use turing_types::{DocumentEpoch, ProcessId, SequenceNumber};

/// Maximum encoded length of a control-plane message in the M0 laboratory.
pub const MAX_CONTROL_MESSAGE_BYTES: usize = 64 * 1024;

/// Error returned while constructing a bounded control envelope.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EnvelopeError {
    /// The declared encoded length exceeded the configured maximum.
    TooLarge {
        /// Declared encoded length.
        actual: usize,
        /// Maximum accepted encoded length.
        maximum: usize,
    },
}

impl fmt::Display for EnvelopeError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::TooLarge { actual, maximum } => {
                write!(
                    formatter,
                    "control message is {actual} bytes; maximum is {maximum} bytes"
                )
            }
        }
    }
}

impl std::error::Error for EnvelopeError {}

/// A typed, bounded message envelope.
///
/// The payload is not serialized by this crate. Subsystem schemas will provide
/// encoding only after the canonical IPC generator is accepted.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ControlEnvelope<T> {
    sender: ProcessId,
    receiver: ProcessId,
    sequence: SequenceNumber,
    document_epoch: Option<DocumentEpoch>,
    encoded_len: usize,
    payload: T,
}

impl<T> ControlEnvelope<T> {
    /// Constructs a bounded message envelope.
    pub fn new(
        sender: ProcessId,
        receiver: ProcessId,
        sequence: SequenceNumber,
        document_epoch: Option<DocumentEpoch>,
        encoded_len: usize,
        payload: T,
    ) -> Result<Self, EnvelopeError> {
        if encoded_len > MAX_CONTROL_MESSAGE_BYTES {
            return Err(EnvelopeError::TooLarge {
                actual: encoded_len,
                maximum: MAX_CONTROL_MESSAGE_BYTES,
            });
        }

        Ok(Self {
            sender,
            receiver,
            sequence,
            document_epoch,
            encoded_len,
            payload,
        })
    }

    /// Returns the sending process identity.
    #[must_use]
    pub const fn sender(&self) -> ProcessId {
        self.sender
    }

    /// Returns the receiving process identity.
    #[must_use]
    pub const fn receiver(&self) -> ProcessId {
        self.receiver
    }

    /// Returns the message sequence number.
    #[must_use]
    pub const fn sequence(&self) -> SequenceNumber {
        self.sequence
    }

    /// Returns the document epoch when the operation is document-scoped.
    #[must_use]
    pub const fn document_epoch(&self) -> Option<DocumentEpoch> {
        self.document_epoch
    }

    /// Returns the declared encoded message length.
    #[must_use]
    pub const fn encoded_len(&self) -> usize {
        self.encoded_len
    }

    /// Returns the typed payload.
    #[must_use]
    pub const fn payload(&self) -> &T {
        &self.payload
    }
}

#[cfg(test)]
mod tests {
    use super::{ControlEnvelope, EnvelopeError, MAX_CONTROL_MESSAGE_BYTES};
    use turing_types::{ProcessId, SequenceNumber};

    #[test]
    fn rejects_oversized_control_messages() {
        let result = ControlEnvelope::new(
            ProcessId::new(1).expect("valid process id"),
            ProcessId::new(2).expect("valid process id"),
            SequenceNumber::new(1).expect("valid sequence"),
            None,
            MAX_CONTROL_MESSAGE_BYTES + 1,
            (),
        );

        assert_eq!(
            result,
            Err(EnvelopeError::TooLarge {
                actual: MAX_CONTROL_MESSAGE_BYTES + 1,
                maximum: MAX_CONTROL_MESSAGE_BYTES,
            })
        );
    }

    #[test]
    fn preserves_typed_routing_metadata() {
        let envelope = ControlEnvelope::new(
            ProcessId::new(7).expect("valid process id"),
            ProcessId::new(9).expect("valid process id"),
            SequenceNumber::new(3).expect("valid sequence"),
            None,
            32,
            "navigation-intent",
        )
        .expect("message is bounded");

        assert_eq!(envelope.sender().get(), 7);
        assert_eq!(envelope.receiver().get(), 9);
        assert_eq!(envelope.sequence().get(), 3);
        assert_eq!(envelope.payload(), &"navigation-intent");
    }
}
