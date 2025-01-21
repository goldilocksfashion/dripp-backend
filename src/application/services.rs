use crate::infrastructure::events::Event;
use crate::infrastructure::storage::StorageService;
use crate::infrastructure::storage::StorageServiceSqlLiteImpl;

/// Base microservice
#[allow(dead_code)]
 trait BaseService<T> {
    async fn create(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    async fn delete(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    async fn update(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    async fn search(&self, query: &str) -> Result<Vec<T>, Box<dyn std::error::Error>>;
}

pub struct EventService<T: StorageService<Event>> {
    pub storage_service: T,
}
/// Generic Event microservice with injectable
impl<T: StorageService<Event>> EventService<T> {
    pub fn new(storage_service: T) -> Self {
        EventService { storage_service }
    }
}
/// Event microservice
impl BaseService<Event> for EventService<StorageServiceSqlLiteImpl> {
    async fn create(&self, event: Event) -> Result<bool, Box<dyn std::error::Error>> {
        let result = self.storage_service.create(event).await;
        return result.map_err(|e| Box::new(e) as Box<dyn std::error::Error>);
    }

    async fn delete(&self, event: Event) -> Result<bool, Box<dyn std::error::Error>> {
        let result = self.storage_service.create(event).await;
        return result.map_err(|e| Box::new(e) as Box<dyn std::error::Error>);
    }

    async fn update(&self, _event: Event) -> Result<bool, Box<dyn std::error::Error>> {
        todo!()
    }

    async fn search(&self, query: &str) -> Result<Vec<Event>, Box<dyn std::error::Error>> {
        let result = self.storage_service.search(query);
        return result.map_err(|e| Box::new(e) as Box<dyn std::error::Error>);
    }
}
