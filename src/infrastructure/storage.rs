use crate::infrastructure::core::TOKIO;
use crate::infrastructure::core::{InfraResult, InfrastructureError};
use crate::infrastructure::env::Environment;
use crate::infrastructure::env::SQLLITE_POOL as DB_POOL;
use crate::infrastructure::events::{Event};
use sqlx::SqlitePool;



/// Storage service is a trait that defines the operations that can be performed on a storage.
pub trait StorageService<T> {
    fn create(&self, event: T) -> impl std::future::Future<Output = InfraResult<bool>> + Send;
    fn delete(&self, event: T) -> impl std::future::Future<Output = InfraResult<bool>> + Send;
    fn search(&self, query: &str) -> InfraResult<Vec<T>>;
}

pub struct StorageServiceSqlLiteImpl {
    _env: Environment,
    db: &'static SqlitePool,
    _runtime: &'static tokio::runtime::Runtime,
}

impl StorageServiceSqlLiteImpl {
    pub fn new(passed_in_env: Environment) -> Self {
        StorageServiceSqlLiteImpl {
            _env: passed_in_env,
            db: &DB_POOL,
            _runtime: &TOKIO,
        }
    }
}

impl StorageService<Event> for StorageServiceSqlLiteImpl {
      async fn create(&self, event: Event) -> InfraResult<bool> {
        let query = r"#INSERT INTO events (id, event_source, created, pinned, event_type, payload) VALUES (?, ?, ?, ?, ?, ?)";
        let r =  sqlx::query(query)
            .bind(event.id.to_vec().as_slice())
            .bind(event.event_source.id.to_vec().as_slice())
            .bind(event.created)
            .bind(event.pinned)
            .bind(event.event_type)
            .bind(event.payload)
            .execute(self.db)
            .await
            .map_err(|e| InfrastructureError::StorageError("Failed to create event".to_string(), Box::new(e)))?;
            return Ok(r.rows_affected() == 1)
    }

    async fn delete(&self, _event: Event) -> Result<bool, InfrastructureError> {
        todo!()
    }
    
    fn search(&self, _query: &str) -> InfraResult<Vec<Event>> {
        todo!()
    }

}
