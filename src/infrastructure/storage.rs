use std::collections::HashMap;

use crate::infrastructure::core::TOKIO;
use crate::infrastructure::core::{InfrasResult, InfrastructureError};
use crate::infrastructure::env::Environment;
use crate::infrastructure::env::SQLLITE_POOL as DB_POOL;
use crate::infrastructure::events::{Event, EventType};
use once_cell::sync::Lazy;
use sqlx::SqlitePool;

use super::core::InfraResult;

/// Persisted data identifying an event source.
#[derive(Debug, Serialize, Deserialize)]
struct Id<'a>{
    public_key: [u8; 32],
    #[serde(skip)] // Skip this field during serialization
    secret_key: &'a [u8],
    created: i64,
}


/// Storage service is a trait that defines the operations that can be performed on a storage.
pub trait StorageService<T: Event> {
    fn create(&self, event: T) -> InfraResult<bool>;
    fn delete(&self, event: T) -> InfraResult<bool>;
    fn search(&self, query: &str) -> InfraResult<Vec>;
}

pub struct StorageServiceSqlLiteImpl {
    env: Environment,
    db: &'static SqlitePool,
    runtime: &'static tokio::runtime::Runtime,
}

pub impl StorageServiceSqlLiteImpl {
    pub fn new(passed_in_env: Environment) -> Self {
        StorageServiceSqlLiteImpl {
            env: passed_in_env,
            db: &DB_POOL,
            runtime: &TOKIO,
        }
    }
}

pub impl StorageService for StorageServiceSqlLiteImpl {
    fn create(&self, event: Event) -> InfrasResult<bool> {
        let query = r"#INSERT INTO events (id, event_source, created, pinned, event_type, payload) VALUES (?, ?, ?, ?, ?, ?)";
        sqlx::query(query)
            .bind(event.id)
            .bind(event.event_source.name)
            .bind(event.created)
            .bind(event.pinned)
            .bind(event.event_type)
            .bind(event.payload)
            .execute(self.db)
            .await?
            .map_err(|e| InfrastructureError::StorageError(("Failed to create event"), (e)))?;
    }

    fn delete(&self, event: Event) -> Result<bool, InfrastructureError> {
        todo!()
    }

    fn update(&self, event: Event) -> Result<bool, InfrastructureError> {
        todo!()
    }

    fn search(&self, query: &str) -> Result<Vec<Event>, InfrastructureError> {
        todo!()
    }
}
