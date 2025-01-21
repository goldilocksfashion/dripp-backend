use std::{collections::HashMap, vec};

use once_cell::sync::Lazy;
use sqlx::{sqlite::SqlitePoolOptions, SqlitePool};
/// A tag is useful to tag on events, environments as additional metadata for anything. This is useful
/// for filtering, searching, and categorizing events for querying,
#[derive(Debug, Default)]
pub struct Tag {
    pub name: String,
    pub value: String,
    pub color: String,
    pub owner: String,
}
#[derive(Debug, Default)]
pub struct Environment {
    pub context: HashMap<String, String>,
    pub tags: Vec<Tag>,
    pub db_name: String,
}

/// Lazy initialization of the environment
pub static DB_ENVIRONMENT: Lazy<Environment> = Lazy::new(|| Environment {
    db_name: "events".to_string(),
    context: HashMap::new(),
    tags: vec![Tag {
        name: "events".to_string(),
        value: "events".to_string(),
        color: "blue".to_string(),
        owner: "system".to_string(),
    }],
});

pub static SQLLITE_POOL: Lazy<SqlitePool> = Lazy::new(|| {
    // This initialization is performed only once
    SqlitePoolOptions::new()
        .max_connections(5) // Set max connections
        .connect_lazy(&format!("sqlite://{}!.db", DB_ENVIRONMENT.db_name))
        .expect("Failed to create database pool")
});
