use crate::core::models::groups::Group;
use crate::core::models::events::Event;
use crate::core::models::events::EventStream;
use crate::core::models::groups::Topic;
use crate::infrastructure::storage::StorageService;
use crate::infrastructure::storage::StorageServiceSqlLiteImpl;



/// Base microservice
pub trait BaseService<T>{
    fn create(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    fn delete(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    fn update(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    fn search(&self, query: &str) -> Result<Vec<T>, Box<dyn std::error::Error>>;
}

pub struct EventService<T: StorageService> {
    pub storage_service: T,
}
/// Generic Event microservice with injectable
pub impl<T: StorageService> EventService<StorageService> {
    pub fn new(storage_service: T) -> Self {
        EventService { storage_service }
    }
}
/// Event microservice
pub impl BaseService<Event> for EventService<StorageServiceSqlLiteImpl> {
    fn create(&self, event: Event) -> Result<bool, Box<dyn std::error::Error>> {
        let result: Result<bool, crate::infrastructure::core::InfrastructureError> = self.storage_service.create(event);
        return result.map_err(|e| Box::new(e) as Box<dyn std::error::Error>);
    }

    fn delete(&self, event: Event) -> Result<bool, Box<dyn std::error::Error>> {
        let result: Result<bool, crate::infrastructure::core::InfrastructureError> = self.storage_service.create(event);
        return result.map_err(|e| Box::new(e) as Box<dyn std::error::Error>);
    }

    fn update(&self, event: Event) -> Result<bool, Box<dyn std::error::Error>> {
        todo!()
    }

    fn search(&self, query: &str) -> Result<Vec<Event>, Box<dyn std::error::Error>> {
        let result: Result<bool, crate::infrastructure::core::InfrastructureError> = self.storage_service.search(query);
        return result.map_err(|e| Box::new(e) as Box<dyn std::error::Error>);
    }
}