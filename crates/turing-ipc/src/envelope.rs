// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use core::fmt;

use turing_types::{ChannelId, DocumentEpoch, OperationId, ProcessIdentity, SequenceNumber};

use crate::{DocumentScope, EncodedSize, MessageKind, PROTOCOL_VERSION};

/// Error returned while constructing a bounded control envelope.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EnvelopeError {
    /// The declared encoded length exceeded the message-kind maximum.
    TooLarge {
        /// Declared encoded length.
        actual: usize,
        /// Maximum accepted encoded length.
        maximum: usize,
    },
    /// A document-scoped message omitted its current document epoch.
    MissingDocumentEpoch {
        /// Message kind requiring the epoch.
        kind: MessageKind,
    },
    /// A process-scoped message carried an unexpected document epoch.
    UnexpectedDocumentEpoch {
        /// Message kind forbidding the epoch.
        kind: MessageKind,
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
            Self::MissingDocumentEpoch { kind } => {
                write!(formatter, "{} requires a document epoch", kind.as_str())
            }
            Self::UnexpectedDocumentEpoch { kind } => {
                write!(formatter, "{} forbids a document epoch", kind.as_str())
            }
        }
    }
}

impl std::error::Error for EnvelopeError {}

/// Typed, bounded metadata and payload for one control-plane message.
///
/// Construction validates the generated size and document-scope contract. The
/// browser kernel separately validates current process epochs, roles,
/// capabilities, routes, and sequence state before dispatch.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ControlEnvelope<T> {
    protocol_version: u16,
    kind: MessageKind,
    sender: ProcessIdentity,
    receiver: ProcessIdentity,
    channel: ChannelId,
    sequence: SequenceNumber,
    operation: OperationId,
    document_epoch: Option<DocumentEpoch>,
    encoded_len: usize,
    payload: T,
}

impl<T> ControlEnvelope<T> {
    /// Constructs an envelope using the current control-plane protocol.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        kind: MessageKind,
        sender: ProcessIdentity,
        receiver: ProcessIdentity,
        channel: ChannelId,
        sequence: SequenceNumber,
        operation: OperationId,
        document_epoch: Option<DocumentEpoch>,
        encoded_len: usize,
        payload: T,
    ) -> Result<Self, EnvelopeError> {
        let maximum = kind.maximum_encoded_bytes();
        if encoded_len > maximum {
            return Err(EnvelopeError::TooLarge {
                actual: encoded_len,
                maximum,
            });
        }

        match (kind.document_scope(), document_epoch) {
            (DocumentScope::Required, None) => {
                return Err(EnvelopeError::MissingDocumentEpoch { kind });
            }
            (DocumentScope::Forbidden, Some(_)) => {
                return Err(EnvelopeError::UnexpectedDocumentEpoch { kind });
            }
            (DocumentScope::Required | DocumentScope::Optional | DocumentScope::Forbidden, _) => {}
        }

        Ok(Self {
            protocol_version: PROTOCOL_VERSION,
            kind,
            sender,
            receiver,
            channel,
            sequence,
            operation,
            document_epoch,
            encoded_len,
            payload,
        })
    }

    /// Returns the control-plane protocol version.
    #[must_use]
    pub const fn protocol_version(&self) -> u16 {
        self.protocol_version
    }

    /// Returns the generated message kind.
    #[must_use]
    pub const fn kind(&self) -> MessageKind {
        self.kind
    }

    /// Returns the restart-safe sender identity.
    #[must_use]
    pub const fn sender(&self) -> ProcessIdentity {
        self.sender
    }

    /// Returns the restart-safe receiver identity.
    #[must_use]
    pub const fn receiver(&self) -> ProcessIdentity {
        self.receiver
    }

    /// Returns the channel identity used for sequence validation.
    #[must_use]
    pub const fn channel(&self) -> ChannelId {
        self.channel
    }

    /// Returns the message sequence number.
    #[must_use]
    pub const fn sequence(&self) -> SequenceNumber {
        self.sequence
    }

    /// Returns the operation identity used for cancellation and tracing.
    #[must_use]
    pub const fn operation(&self) -> OperationId {
        self.operation
    }

    /// Returns the document epoch when the schema allows one.
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

    /// Consumes the envelope and returns its payload.
    #[must_use]
    pub fn into_payload(self) -> T {
        self.payload
    }
}

impl<T> EncodedSize for ControlEnvelope<T> {
    fn encoded_len(&self) -> usize {
        self.encoded_len
    }
}

#[cfg(test)]
mod tests {
    use super::{ControlEnvelope, EnvelopeError};
    use crate::MessageKind;
    use turing_types::{
        ChannelId, DocumentEpoch, OperationId, ProcessEpoch, ProcessId, ProcessIdentity,
        SequenceNumber,
    };

    fn process(id: u64) -> ProcessIdentity {
        ProcessIdentity::new(
            ProcessId::new(id).expect("valid process id"),
            ProcessEpoch::new(1).expect("valid process epoch"),
        )
    }

    #[test]
    fn rejects_message_larger_than_generated_kind_limit() {
        let kind = MessageKind::NavigationIntent;
        let result = ControlEnvelope::new(
            kind,
            process(1),
            process(2),
            ChannelId::new(1).expect("valid channel"),
            SequenceNumber::new(1).expect("valid sequence"),
            OperationId::new(1).expect("valid operation"),
            Some(DocumentEpoch::new(1).expect("valid document epoch")),
            kind.maximum_encoded_bytes() + 1,
            (),
        );

        assert_eq!(
            result,
            Err(EnvelopeError::TooLarge {
                actual: kind.maximum_encoded_bytes() + 1,
                maximum: kind.maximum_encoded_bytes(),
            })
        );
    }

    #[test]
    fn enforces_generated_document_scope() {
        let result = ControlEnvelope::new(
            MessageKind::NavigationIntent,
            process(1),
            process(2),
            ChannelId::new(1).expect("valid channel"),
            SequenceNumber::new(1).expect("valid sequence"),
            OperationId::new(1).expect("valid operation"),
            None,
            64,
            (),
        );

        assert_eq!(
            result,
            Err(EnvelopeError::MissingDocumentEpoch {
                kind: MessageKind::NavigationIntent,
            })
        );
    }
}
