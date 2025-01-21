use crate::core::models::groups::Group;
use crate::core::models::events::Event;
use crate::core::models::events::EventStream;
use crate::core::models::groups::Topic;


/// Base manager for all services
trait BaseManager<T>{
    fn create(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    fn delete(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    fn update(&self, event: T) -> Result<bool, Box<dyn std::error::Error>>;
    fn search(&self, query: &str) -> Result<Vec<T>, Box<dyn std::error::Error>>;
}
