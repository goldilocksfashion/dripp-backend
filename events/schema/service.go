package schema

import (
    "database/sql"
    "fmt"
    "log"
    "net/http"
    "time"
    "shared-libraries/http"
    "shared-libraries/k8s"

    "github.com/jmoiron/sqlx"
    _ "github.com/go-sql-driver/mysql"
)


func main() {
    server := http.NewServer("events/schema")
    schemaRegistry, err := NewSchemaRegistry()
    if err != nil {
        log.Fatalf("Failed to create schema registry: %s", err)
    }

    server.AddHandler("/schema", func(w http.ResponseWriter, r *http.Request) {
        sourceContext := r.URL.Query().Get("source_context")
        version := r.URL.Query().Get("version")
        if sourceContext == "" || version == "" {
            http.Error(w, "source_context and version are required query parameters", http.StatusBadRequest)
            return
        }

        schema, err := schemaRegistry.GetSchema(sourceContext, version)
        if err != nil {
            http.Error(w, fmt.Sprintf("Failed to get schema: %s", err), http.StatusInternalServerError)
            return
        }

        w.Write([]byte(schema.Schema))
    })

    server.StartServer("8080")
}
