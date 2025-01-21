use std::error::Error as StdError;
use thiserror::Error;
use tokio::runtime::Runtime;
use once_cell::sync::Lazy;

/// Error enum for Infrastructure layer
#[derive(Debug, Error)]
pub enum InfrastructureError {
    /// Error for storage layer
    #[error("Storage error: {0}")]
    StorageError(String, #[source] Box<dyn StdError + Send + Sync>),
    /// Error for event layer
    #[error("Event error: {0}")]
    EventError(String, #[source] Box<dyn StdError + Send + Sync>),
    /// Error for core layer
    #[error("Core error: {0}")]
    CoreError(String, #[source] Box<dyn StdError + Send + Sync>),
    /// Error for env layer
    #[error("Env error: {0}")]
    EnvError(String, #[source] Box<dyn StdError + Send + Sync>),
    /// Error for unknown error
    #[error("Unknown error: {0}")]
    UnknownError(String, #[source] Box<dyn StdError + Send + Sync>),
}

/// Result type for Infrastructure layer
pub type InfraResult<T> = std::result::Result<T, InfrastructureError>;

/// Lazy static instance of tokio runtime
pub static TOKIO: Lazy<Runtime> = Lazy::new(|| {
    let rt = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap();
    rt
});
