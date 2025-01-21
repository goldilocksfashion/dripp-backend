use std::collections::VecDeque;

use serde::{Deserialize, Serialize};
use derive_builder::Builder;

/// An event source can be group, a user, a bot or a device or a system.
#[derive(Builder, Debug, Serialize, Deserialize,  Clone)]
pub struct EventSource<'a> {
    pub id: &'a [u8],
    pub name: &'a str,
    pub created: i64,
    pub last_updated: i64,
}


// An event is an immutable captured frame from event source.
#[derive(Builder, Debug, Serialize, Deserialize,Clone)]
pub struct Event<'a>{
    pub id: &'a [u8],
    pub event_source: EventSource<'a>,
    pub created: i64,
    pub pinned: bool,
    pub event_type: &'a [u8],
    pub payload: &'a [u8],
}


pub struct EventStream<'a>{
    pub id: &'a [u8],
    pub name:  &'a [u8],
    pub created: i64,
    pub last_updated: i64,
    pub event_buffer: VecDeque<Event<'a>>,
    pub event_source: EventSource<'a>,
}
