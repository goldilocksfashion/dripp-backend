use rocksdb::{DB, Options};
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
struct Id{
    public_key: Vec<u8>,
    #[serde(skip)] // Skip this field during serialization
    secret_key: Vec<u8>,
    created: i64,
}




/// A group is a collection members with a common interest.
pub struct Group{
    id: Vec<u8>,
    name: String,
    created: i64,
    last_updated: i64,
    is_private: bool,
    dicussion: EventStream,
    members: EventStream,
    media: EventStream,
    files: EventStream
}

/// e.g. fashion, vintage-cars, programming, cooking, etc.
pub struct Topic {
    id: Vec<u8>,
    name: String,
    created: i64,
    last_updated: i64,
    groups: Vec<Group> 
}
