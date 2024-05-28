package schema

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	"github.com/jmoiron/sqlx"
	"k8s.io/client-go/kubernetes"
)

// SchemaRegistry represents a schema registry.
type SchemaRegistry struct {
	DB *sqlx.DB
}

// NewSchemaRegistry creates a new instance of SchemaRegistry.
func NewSchemaRegistry() (*SchemaRegistry, error) {
	k8sClient := k8s.GetInstance()
	conf, err := k8sClient.GetConfigMap("schema-registry-config")
	config := conf.Data
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", config["DB_USER"], config["DB_PASSWORD"], config["DB_HOST"], config["DB_PORT"], config["DB_NAME"])
	db, err := sqlx.Connect("mysql", dsn)
	if err != nil {
		log.Fatalf("Failed to connect to database: %s", err)
	}
	defer db.Close()

	// Set maximum number of open connections
	db.SetMaxOpenConns(0)
	// Set maximum number of idle connections
	db.SetMaxIdleConns(25)
	// Set the maximum lifetime of a connection
	db.SetConnMaxLifetime(5 * time.Minute)

	if err != nil {
		return nil, err
	}

	return &SchemaRegistry{DB: db}, nil
}

// RegisterSchema registers a new schema in the schema registry.
func (sr *SchemaRegistry) RegisterSchema(sourceContext, schema string, version int) error {
	query := `INSERT INTO event_schemas (source_context, version, schema) VALUES (?, ?, ?)`
	_, err := sr.DB.Exec(query, sourceContext, version, schema)
	return err
}

// GetSchema retrieves a specific schema from the schema registry based on the source context and version.
func (sr *SchemaRegistry) GetSchema(sourceContext string, version int) (EventSchema, error) {
	var schema EventSchema
	query := `SELECT * FROM event_schemas WHERE source_context = ? AND version = ?`
	err := sr.DB.Get(&schema, query, sourceContext, version)
	return schema, err
}

// GetLatestSchema retrieves the latest schema from the schema registry based on the source context.
func (sr *SchemaRegistry) GetLatestSchema(sourceContext string) (EventSchema, error) {
	var schema EventSchema
	query := `SELECT * FROM event_schemas WHERE source_context = ? ORDER BY version DESC LIMIT 1`
	err := sr.DB.Get(&schema, query, sourceContext)
	return schema, err
}
