use crate::application::services::EventService;
use crate::infrastructure::events::Event;
use crate::infrastructure::storage::{StorageService, StorageServiceSqlLiteImpl};
use serde::{Deserialize, Serialize};
use std::ffi::{CStr, CString};
use std::os::raw::c_char;
/// FFI manager manages crud stuff 
/// see: `[services]`
trait FFIManager<T> {
    fn create(&self, event: T) -> FfiResult;
    fn delete(&self, event: T) -> FfiResult;
    fn update(&self, event: T) -> FfiResult;
    fn search(&self, query: *const c_char) -> FfiResult;
}
#[repr(C)]
pub struct FfiResult {
    pub success: bool,              // Indicates if the operation was successful
    pub data: *mut c_char,          // Serialized JSON string (null if error)
    pub error_message: *mut c_char, // Error message (null if success)
}

pub fn to_ffi_result<T: Serialize>(
    result: Result<T, Box<dyn std::error::Error>>,
) -> FfiResult {
    match result {
        Ok(data) => {
            let json = match serde_json::to_string(&data) {
                Ok(json) => json,
                Err(err) => {
                    return FfiResult {
                        success: false,
                        data: std::ptr::null_mut(),
                        error_message: CString::new(err.to_string()).unwrap().into_raw(),
                    };
                }
            };
            FfiResult {
                success: true,
                data: CString::new(json).unwrap().into_raw(),
                error_message: std::ptr::null_mut(),
            }
        }
        Err(err) => FfiResult {
            success: false,
            data: std::ptr::null_mut(),
            error_message: CString::new(err.to_string()).unwrap().into_raw(),
        },
    }
}

#[no_mangle]
pub extern "C" fn free_ffi_result(result: FfiResult) {
    if !result.data.is_null() {
        unsafe { CString::from_raw(result.data) };
    }
    if !result.error_message.is_null() {
        unsafe { CString::from_raw(result.error_message) };
    }
}
impl FFIManager<Event> for EventService<StorageServiceSqlLiteImpl> {
    fn create(&self, event: Event) -> FfiResult {
        let result = self.storage_service.create(event); // Calls storage_service's `create`
        to_ffi_result(result.map(|_| vec![])) // Convert to FfiResult
    }

    fn delete(&self, event: Event) -> FfiResult {
        let result = self.storage_service.delete(event);
        to_ffi_result(result.map(|_| vec![]))
    }

    fn update(&self, event: Event) -> FfiResult {
        let result = self.storage_service.update(event);
        to_ffi_result(result.map(|_| vec![]))
    }

    fn search(&self, query: *const c_char) -> FfiResult {
        let query_str = unsafe {
            if query.is_null() {
                return FfiResult {
                    success: false,
                    data: std::ptr::null_mut(),
                    error_message: CString::new("Query string is null").unwrap().into_raw(),
                };
            }
            CStr::from_ptr(query).to_str().unwrap_or("")
        };

        let result = self.storage_service.search(query_str);
        to_ffi_result(result)
    }
}
