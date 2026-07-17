// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![forbid(unsafe_code)]

mod envelope;
mod generated;
mod queue;
mod sequence;

pub use envelope::{ControlEnvelope, EnvelopeError};
pub use generated::{
    Capability, DocumentScope, MAX_REGISTERED_PROCESSES, MessageKind, PROTOCOL_VERSION,
    ProcessRole, QueueClass,
};
pub use queue::{BoundedQueue, QueueErrorKind, QueuePushError};
pub use sequence::{SequenceError, SequenceTracker};

/// Reports the encoded-byte charge used by bounded queues.
pub trait EncodedSize {
    /// Returns the complete encoded size charged to the queue budget.
    fn encoded_len(&self) -> usize;
}
