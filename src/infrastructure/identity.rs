use crate::infrastructure::core::InfrastructureError;
use crate::infrastructure::env::{Environment, ROCKSDB};
use serde::{Deserialize, Serialize};

use super::core::TOKIO_BLOCKING;
use super::storage::StorageService;

pub struct StorageServiceRocksDBImpl {
    _env: Environment,
    _db: &'static rocksdb::DB,
    _tokio: &'static tokio::runtime::Runtime,
}

impl StorageServiceRocksDBImpl {
    pub fn new(passed_in_env: Environment) -> Self {
        StorageServiceRocksDBImpl {
            _env: passed_in_env,
            _db: &ROCKSDB,
            _tokio: &TOKIO_BLOCKING,
        }
    }
}
impl StorageService<IdentityBlock> for StorageServiceRocksDBImpl {
    async fn create(&self, event: IdentityBlock) -> Result<bool, InfrastructureError> {
        let serialized_event = match bincode::serialize(&event) {
            Ok(data) => data,
            Err(e) => {
                return Err(InfrastructureError::SerializationError(
                    "Serialization error".to_string(),
                    e,
                ));
            }
        };

        // Use async block to wrap the blocking operation
        let result = TOKIO_BLOCKING
            .spawn_blocking(move || {
                // Perform the RocksDB put operation
                ROCKSDB
                    .put(event.block_id, serialized_event)
                    .map(|_| true) // On success, return `true`
                    .map_err(|e| {
                        InfrastructureError::StorageError(
                            "Failed to write to RocksDB".to_string(),
                            Box::new(e),
                        )
                    }) // Map RocksDB errors to `InfrastructureError`
            })
            .await;
        return result.unwrap();
    }

    async fn delete(&self, _event: IdentityBlock) -> Result<bool, InfrastructureError> {
        todo!()
    }

    fn search(&self, _query: &str) -> Result<Vec<IdentityBlock>, InfrastructureError> {
        todo!()
    }
}
