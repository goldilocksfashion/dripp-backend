// use std::os::raw::c_char;
// use once_cell::sync::OnceCell;
// use tokio::runtime::{Builder, Runtime};

// // Global runtime for Tokio
// static RUNTIME: OnceCell<Runtime> = OnceCell::new();

// #[no_mangle]
// pub extern "C" fn init_dripp() -> bool {
//     RUNTIME.set(
//         Builder::new_current_thread() // Use a lightweight single-threaded runtime
//             .enable_all()             // Enable features like time, I/O, etc.
//             .build()
//             .expect("Failed to create Tokio runtime"),
//     ).is_ok()
// }

// /// FFI Payload struct
// /// This struct is used to pass data between Rust and Dart
// #[repr(C)]
// pub struct FFIPayload {
//     pub version: u16,
//     pub signature: *mut u8,  /// Pointer to cryptographic signature
//     pub sig_len: usize,     /// Length of the signature
//     pub content_type: u8,         // Content type (e.g., 0 = Text, 1 = Image, 2 = Video, 3 = Mixed)
//     pub data: *mut u8,                // Pointer to raw data (binary for media or JSON for mixed content)
//     pub data_len: usize,          // Length of the raw data
//     pub metadata: *mut c_char,    // Additional metadata (C string, e.g., JSON with timestamps, user info)
//     pub status: i32,              // Status code for the operation
//     pub success: bool,            // Operation success flag
// }

mod infrastructure;