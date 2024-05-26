CREATE DATABASE schema_registry;

USE schema_registry;

CREATE TABLE event_schemas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_context VARCHAR(255) NOT NULL,
    version INT NOT NULL,
    schema TEXT NOT NULL,
    UNIQUE(source_context, version)
);
