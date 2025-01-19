use rocksdb::{DB, Options};
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
struct Id{
    public_key: Vec<u8>,
    #[serde(skip)] // Skip this field during serialization
    secret_key: Vec<u8>,
    created: i64,
}
trait Storage<T>{
    fn save(&self,key: &str, t: &T) -> Result<bool, ErBox<dyn std::error::Error>>;
    fn get(&self, key: &str) -> Result<Option<T>, Box<dyn std::error::Error>>;
    fn delete(&self, key: &str) -> Result<bool, Box<dyn std::error::Error>>;
}
/// An event source can be group, a user, a bot or a device or a system.
struct EventSource {
    id: Vec<u8>,
    name: String,
    created: i64,
    last_updated: i64,
}



#[derive(Debug, Serialize, Deserialize)]
enum EventType {
    Post { content: Vec<u8> },
    MediaUpload { url: String, file_type: String },
    Membership { user_id: String, action: String }
    ScheduledEvent { event_id: String, venue: String, date_time: DateTime<Utc> }
}


// An event is an immutable captured frame from event source.
struct Event{
    id: Vec<u8>,
    event_source: EventSource,
    created: i64,
    pinned: bool,
    event_type: EventType,
    payload: Vec<u8>,
}

struct EventStream{
    id: Vec<u8>,
    name: String,
    created: i64,
    last_updated: i64,
    event_buffer: Vec<Event>,
    event_source: EventSource,
    storage: Option<DB>
}

/// A group is a collection members with a common interest.
struct Group{
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
struct Topic {
    id: Vec<u8>,
    name: String,
    created: i64,
    last_updated: i64,
    groups: Vec<Group> 
}