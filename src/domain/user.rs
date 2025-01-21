use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: [u8; 16],
    name: String,
    phone: [u8; 10],
    created_at: i64,
}