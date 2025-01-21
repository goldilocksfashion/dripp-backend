use std::{collections::VecDeque, time};

use derive_builder::Builder;
use serde::{Deserialize, Serialize};

const RING_BUFFER_THRESHOLD: usize = 10;

/// An event source can be group, a user, a bot or a device or a system.
#[derive(Builder, Debug, Serialize, Deserialize, Clone)]
pub struct EventSource {
    pub id: [u8; 16],
    pub created: i64,
    pub last_updated: i64,
}

// An event is an immutable captured frame from event source.
#[derive(Builder, Debug, Serialize, Deserialize, Clone)]
pub struct Event {
    pub id: [u8; 16],
    pub event_source: EventSource,
    pub created: i64,
    pub pinned: bool,
    pub event_type: Vec<u8>,
    pub payload: Vec<u8>,
}

#[derive(Builder, Debug, Serialize, Deserialize, Clone)]
/// An event stream is a collection of events.
pub struct EventStream {
    pub id: [u8; 16],
    pub created: i64,
    pub last_updated: i64,
    pub event_buffer: VecDeque<Event>,
    pub event_source: EventSource,
}

/// pre-allocated memory for event stream using ring buffer.
impl EventStream {
    pub fn new(capacity: usize) -> Self {
        EventStream {
            id: [0; 16],
            created: 0,
            last_updated: 0,
            event_buffer: VecDeque::with_capacity(capacity),
            event_source: EventSource {
                id: [0; 16],
                created: 0,
                last_updated: 0,
            },
        }
    }
    pub fn add_event(&mut self, event: Event) {
        if self.event_buffer.len() >= RING_BUFFER_THRESHOLD {
            self.event_buffer.pop_front();
        }
        self.event_buffer.push_back(event);
    }

    pub fn current_size(&self) -> usize {
        self.event_buffer.len()
    }
}
