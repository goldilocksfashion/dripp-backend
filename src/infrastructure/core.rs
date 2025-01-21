use std::fmt::Error;
use thiserror::Error;
use std::error::Error;
use tokio::runtime::Runtime;
use once_cell::sync::Lazy;

pub type  BoxedErr =  Box<dyn Error + Send + Sync>;
/// Error enum for Infrastructure layer
#[derive(Debug, Error)]
pub enum InfrastructureError {
    /// Error for storage layer
    #[error("Storage error: {0}")]
    StorageError(String, #[source] BoxedErr),
    /// Error for event layer
    #[error("Event error: {0}")]
    EventError(String, #[source] BoxedErr),
    /// Error for core layer
    #[error("Core error: {0}")]
    CoreError(String, #[source] BoxedErr),
    /// Error for env layer
    #[error("Env error: {0}")]
    EnvError(String, #[source] BoxedErr),
    /// Error for unknown error
    #[error("Unknown error: {0}")]
    UnknownError(String, #[source] BoxedErr),
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
