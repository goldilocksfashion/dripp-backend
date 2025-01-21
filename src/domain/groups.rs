use serde::{Serialize, Deserialize};
use crate::infrastructure::events::EventStream;


/// A group is a collection members with a common interest.
pub struct Group{
    id: [u8; 16],
    name: Vec<u8>,
    created: i64,
    last_updated: i64,
    is_private: bool,
    dicussion: EventStream,
    members: EventStream,
    media: EventStream,
    files: EventStream,
}

/// e.g. fashion, vintage-cars, programming, cooking, etc.
pub struct Topic {
    id: [u8; 16],
    name: Vec<u8>,
    created: i64,
    last_updated: i64,
    groups: Vec<Group>
}
