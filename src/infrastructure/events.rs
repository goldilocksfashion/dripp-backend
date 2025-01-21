use std::collections::VecDeque;

use derive_builder::Builder;
use serde::{Deserialize, Serialize};

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
