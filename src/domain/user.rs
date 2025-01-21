use serde::{Serialize, Deserialize};


#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: i32,
    name: String,
    phone: String,
    created_at: String,
}