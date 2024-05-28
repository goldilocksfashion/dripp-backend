package schema

// SchemaRegistryInterface defines the interface for interacting with the schema registry.
type SchemaRegistryInterface interface {
	// GetSchema retrieves the event schema for the given source context and version.
	// It returns the event schema and an error if any.
	GetSchema(sourceContext string, version int) (EventSchema, error)

	// GetLatestSchema retrieves the latest event schema for the given source context.
	// It returns the event schema and an error if any.
	GetLatestSchema(sourceContext string) (EventSchema, error)
}

// SchemaRegistry represents the schema registry.
type SchemaRegistry struct {
	DB *sqlx.DB
}

// EventSchema represents the structure of an event schema.
type EventSchema struct {
	ID            int    `db:"id"`
	SourceContext string `db:"source_context"`
	Version       int    `db:"version"`
	Schema        string `db:"schema"`
}
