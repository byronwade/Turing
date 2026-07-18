// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use core::fmt;

use turing_types::SequenceNumber;

/// Error returned when a channel receives an invalid sequence number.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SequenceError {
    /// The first message on a channel did not use sequence one.
    InvalidFirst {
        /// Sequence that was received.
        actual: SequenceNumber,
    },
    /// The sequence was already accepted or predates the current channel state.
    DuplicateOrOld {
        /// Last accepted sequence.
        last: SequenceNumber,
        /// Sequence that was received.
        actual: SequenceNumber,
    },
    /// One or more messages were skipped.
    Gap {
        /// Sequence that should have arrived next.
        expected: SequenceNumber,
        /// Sequence that was received.
        actual: SequenceNumber,
    },
    /// The channel sequence reached its maximum representable value.
    Exhausted,
}

impl fmt::Display for SequenceError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidFirst { actual } => {
                write!(
                    formatter,
                    "first channel sequence must be 1, received {actual}"
                )
            }
            Self::DuplicateOrOld { last, actual } => {
                write!(
                    formatter,
                    "channel already accepted sequence {last}; received {actual}"
                )
            }
            Self::Gap { expected, actual } => {
                write!(
                    formatter,
                    "expected channel sequence {expected}, received {actual}"
                )
            }
            Self::Exhausted => formatter.write_str("channel sequence is exhausted"),
        }
    }
}

impl std::error::Error for SequenceError {}

/// Exact, monotonic receive-side sequence state for one IPC channel.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct SequenceTracker {
    last_accepted: Option<SequenceNumber>,
}

impl SequenceTracker {
    /// Creates an empty channel sequence tracker.
    #[must_use]
    pub const fn new() -> Self {
        Self {
            last_accepted: None,
        }
    }

    /// Returns the last sequence accepted by the channel.
    #[must_use]
    pub const fn last_accepted(self) -> Option<SequenceNumber> {
        self.last_accepted
    }

    /// Accepts exactly the next sequence without mutating state on failure.
    pub fn accept(&mut self, actual: SequenceNumber) -> Result<(), SequenceError> {
        let expected = match self.last_accepted {
            None => SequenceNumber::new(1).expect("one is non-zero"),
            Some(last) => last.checked_next().ok_or(SequenceError::Exhausted)?,
        };

        if actual == expected {
            self.last_accepted = Some(actual);
            return Ok(());
        }

        match self.last_accepted {
            Some(last) if actual <= last => Err(SequenceError::DuplicateOrOld { last, actual }),
            None => Err(SequenceError::InvalidFirst { actual }),
            Some(_) => Err(SequenceError::Gap { expected, actual }),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{SequenceError, SequenceTracker};
    use turing_types::SequenceNumber;

    #[test]
    fn accepts_exactly_monotonic_sequences() {
        let mut tracker = SequenceTracker::new();
        tracker
            .accept(SequenceNumber::new(1).expect("valid sequence"))
            .expect("first sequence is valid");
        tracker
            .accept(SequenceNumber::new(2).expect("valid sequence"))
            .expect("second sequence is valid");
        assert_eq!(tracker.last_accepted().expect("sequence exists").get(), 2);
    }

    #[test]
    fn rejects_gaps_without_advancing_state() {
        let mut tracker = SequenceTracker::new();
        tracker
            .accept(SequenceNumber::new(1).expect("valid sequence"))
            .expect("first sequence is valid");
        let actual = SequenceNumber::new(3).expect("valid sequence");
        assert_eq!(
            tracker.accept(actual),
            Err(SequenceError::Gap {
                expected: SequenceNumber::new(2).expect("valid sequence"),
                actual,
            })
        );
        assert_eq!(tracker.last_accepted().expect("sequence exists").get(), 1);
    }
}
