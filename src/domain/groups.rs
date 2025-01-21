use serde::{Serialize, Deserialize};
use crate::infrastructure::events::EventStream;


/// A group is a collection members with a common interest.
#[derive(Serialize, Deserialize)]
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
#[derive(Serialize, Deserialize)]
pub struct Topic {
    id: [u8; 16],
    name: Vec<u8>,
    created: i64,
    last_updated: i64,
    groups: Vec<Group>
}

#[cfg(test)]
mod tests{
    use std::collections::VecDeque;

    use crate::infrastructure::events::{EventSourceBuilder, EventStreamBuilder};

    use super::*;
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn test_group_serialization_roundtrip(
            id in prop::array::uniform16(any::<u8>()),
            name in prop::collection::vec(any::<u8>(), 0..100),
            created in any::<i64>(),
            last_updated in any::<i64>(),
            is_private in any::<bool>(),
        ) {
            let mock_stream = EventStreamBuilder::default()
            .id([1; 16])
            .created(1627683940)
            .last_updated(1627684000)
            .event_buffer(VecDeque::new())
            .event_source(EventSourceBuilder::default()
            .id([1; 16])
            .created(1627683940)
            .last_updated(1627684000).build().expect("Failed to build EventSource"))
            .build()
            .expect("Failed to build EventStream");

            let group = Group {
                id,
                name,
                created,
                last_updated,
                is_private,
                dicussion: mock_stream.clone(),
                members: mock_stream.clone(),
                media: mock_stream.clone(),
                files: mock_stream,
            };

            let serialized = serde_json::to_string(&group).expect("Serialization failed");
            let deserialized: Group = serde_json::from_str(&serialized).expect("Deserialization failed");

            prop_assert_eq!(group.id, deserialized.id);
            prop_assert_eq!(group.name, deserialized.name);
            prop_assert_eq!(group.created, deserialized.created);
            prop_assert_eq!(group.last_updated, deserialized.last_updated);
            prop_assert_eq!(group.is_private, deserialized.is_private);
        }
    }
}
