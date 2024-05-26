package schema

import (
    "database/sql"
    "fmt"
    "log"
	"shared-libraries/k8s"

    "github.com/jmoiron/sqlx"
    _ "github.com/go-sql-driver/mysql"
)

type SchemaRegistryInterface interface {
    GetSchema(sourceContext string, version int) (EventSchema, error)
    GetLatestSchema(sourceContext string) (EventSchema, error)
}
type SchemaRegistry struct {
    DB *sqlx.DB
}

type EventSchema struct {
    ID            int    `db:"id"`
    SourceContext string `db:"source_context"`
    Version       int    `db:"version"`
    Schema        string `db:"schema"`
}

func NewSchemaRegistry(dsn string) (*SchemaRegistry, error) {
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

func (sr *SchemaRegistry) RegisterSchema(sourceContext, schema string, version int) error {
    query := `INSERT INTO event_schemas (source_context, version, schema) VALUES (?, ?, ?)`
    _, err := sr.DB.Exec(query, sourceContext, version, schema)
    return err
}

func (sr *SchemaRegistry) GetSchema(sourceContext string, version int) (EventSchema, error) {
    var schema EventSchema
    query := `SELECT * FROM event_schemas WHERE source_context = ? AND version = ?`
    err := sr.DB.Get(&schema, query, sourceContext, version)
    return schema, err
}

func (sr *SchemaRegistry) GetLatestSchema(sourceContext string) (EventSchema, error) {
    var schema EventSchema
    query := `SELECT * FROM event_schemas WHERE source_context = ? ORDER BY version DESC LIMIT 1`
    err := sr.DB.Get(&schema, query, sourceContext)
    return schema, err
}
