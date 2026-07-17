// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

use std::collections::VecDeque;

use crate::{EncodedSize, QueueClass};

/// Reason a bounded queue rejected an item.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum QueueErrorKind {
    /// The item cannot fit within the queue's byte budget even when empty.
    ItemTooLarge {
        /// Encoded item length.
        actual: usize,
        /// Queue byte budget.
        maximum: usize,
    },
    /// The queue reached its item-count budget.
    ItemLimit {
        /// Maximum item count.
        maximum: usize,
    },
    /// Accepting the item would exceed the queue's byte budget.
    ByteLimit {
        /// Current queued bytes.
        current: usize,
        /// Incoming encoded bytes.
        incoming: usize,
        /// Maximum queued bytes.
        maximum: usize,
    },
    /// Byte accounting overflowed before a policy decision could be made.
    ByteCounterOverflow,
}

/// A rejected queue item returned to its caller without being dropped.
#[derive(Debug)]
pub struct QueuePushError<T> {
    kind: QueueErrorKind,
    item: T,
}

impl<T> QueuePushError<T> {
    /// Returns the rejection reason.
    #[must_use]
    pub const fn kind(&self) -> QueueErrorKind {
        self.kind
    }

    /// Returns the rejected item to the caller.
    #[must_use]
    pub fn into_item(self) -> T {
        self.item
    }
}

/// FIFO queue with generated item and byte budgets and explicit backpressure.
#[derive(Clone, Debug)]
pub struct BoundedQueue<T> {
    class: QueueClass,
    queued_bytes: usize,
    items: VecDeque<T>,
}

impl<T> BoundedQueue<T> {
    /// Creates an empty queue for the generated budget class.
    #[must_use]
    pub fn new(class: QueueClass) -> Self {
        Self {
            class,
            queued_bytes: 0,
            items: VecDeque::new(),
        }
    }

    /// Returns the queue class.
    #[must_use]
    pub const fn class(&self) -> QueueClass {
        self.class
    }

    /// Returns the current item count.
    #[must_use]
    pub fn len(&self) -> usize {
        self.items.len()
    }

    /// Returns whether the queue is empty.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }

    /// Returns the current encoded-byte charge.
    #[must_use]
    pub const fn queued_bytes(&self) -> usize {
        self.queued_bytes
    }
}

impl<T: EncodedSize> BoundedQueue<T> {
    /// Attempts to append an item without blocking or silently evicting work.
    pub fn try_push(&mut self, item: T) -> Result<(), QueuePushError<T>> {
        let incoming = item.encoded_len();
        let maximum_bytes = self.class.maximum_queued_bytes();
        if incoming > maximum_bytes {
            return Err(QueuePushError {
                kind: QueueErrorKind::ItemTooLarge {
                    actual: incoming,
                    maximum: maximum_bytes,
                },
                item,
            });
        }

        let maximum_items = self.class.maximum_items();
        if self.items.len() >= maximum_items {
            return Err(QueuePushError {
                kind: QueueErrorKind::ItemLimit {
                    maximum: maximum_items,
                },
                item,
            });
        }

        let Some(next_bytes) = self.queued_bytes.checked_add(incoming) else {
            return Err(QueuePushError {
                kind: QueueErrorKind::ByteCounterOverflow,
                item,
            });
        };
        if next_bytes > maximum_bytes {
            return Err(QueuePushError {
                kind: QueueErrorKind::ByteLimit {
                    current: self.queued_bytes,
                    incoming,
                    maximum: maximum_bytes,
                },
                item,
            });
        }

        self.items.push_back(item);
        self.queued_bytes = next_bytes;
        Ok(())
    }

    /// Removes the oldest item and releases its byte charge.
    pub fn pop_front(&mut self) -> Option<T> {
        let item = self.items.pop_front()?;
        self.queued_bytes = self
            .queued_bytes
            .checked_sub(item.encoded_len())
            .expect("queued byte accounting is internally consistent");
        Some(item)
    }
}

#[cfg(test)]
mod tests {
    use super::{BoundedQueue, QueueErrorKind};
    use crate::{EncodedSize, QueueClass};

    #[derive(Clone, Debug, Eq, PartialEq)]
    struct SizedItem(usize);

    impl EncodedSize for SizedItem {
        fn encoded_len(&self) -> usize {
            self.0
        }
    }

    #[test]
    fn applies_byte_backpressure_without_dropping_item() {
        let mut queue = BoundedQueue::new(QueueClass::Urgent);
        queue
            .try_push(SizedItem(QueueClass::Urgent.maximum_queued_bytes()))
            .expect("first item fills byte budget");
        let error = queue
            .try_push(SizedItem(1))
            .expect_err("next item exceeds byte budget");
        assert_eq!(
            error.kind(),
            QueueErrorKind::ByteLimit {
                current: QueueClass::Urgent.maximum_queued_bytes(),
                incoming: 1,
                maximum: QueueClass::Urgent.maximum_queued_bytes(),
            }
        );
        assert_eq!(error.into_item(), SizedItem(1));
    }

    #[test]
    fn releases_byte_charge_when_item_is_popped() {
        let mut queue = BoundedQueue::new(QueueClass::Control);
        queue.try_push(SizedItem(32)).expect("item fits");
        assert_eq!(queue.queued_bytes(), 32);
        assert_eq!(queue.pop_front(), Some(SizedItem(32)));
        assert_eq!(queue.queued_bytes(), 0);
    }
}
