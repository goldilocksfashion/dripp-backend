package http

import (
	"io"
	"log"
	"net/http"
	"net/url"
	"sync"
)

// Server is an interface that defines the behavior of an HTTP server.
type Server interface {
	StartServer(port string, boundedContext string)
	// AddHandler adds a new handler function to the server for the specified path.
	// Example usage:
	//  server := http.NewServer("events/schema")
    // schemaRegistry, err := NewSchemaRegistry()
    // if err != nil {
    //     log.Fatalf("Failed to create schema registry: %s", err)
    // }

    // server.AddHandler("/schema", func(w http.ResponseWriter, r *http.Request) {
    //     sourceContext := r.URL.Query().Get("source_context")
    //     version := r.URL.Query().Get("version")
    //     if sourceContext == "" || version == "" {
    //         http.Error(w, "source_context and version are required query parameters", http.StatusBadRequest)
    //         return
    //     }

    //     schema, err := schemaRegistry.GetSchema(sourceContext, version)
    //     if err != nil {
    //         http.Error(w, fmt.Sprintf("Failed to get schema: %s", err), http.StatusInternalServerError)
    //         return
    //     }

    //     w.Write([]byte(schema.Schema))
    // })
	AddHandler(path string, handler http.HandlerFunc)
}

// Request represents an HTTP request.
type Request struct {
	Method string
	URL    *url.URL
	Header map[string][]string
	Body   io.ReadCloser
}

// ResponseWriter is an interface that represents an HTTP response writer.
type ResponseWriter interface {
	http.ResponseWriter
}

// serverImpl is an implementation of the Server interface.
type serverImpl struct {
	boundedContext string
	mux *http.ServeMux
	wg  sync.WaitGroup
}

// NewServer creates a new instance of the serverImpl struct.
func NewServer(boundedContext string) Server {
	return &serverImpl{
		boundedContext: boundedContext,
		mux: http.NewServeMux(),
	}
}

// StartServer starts the HTTPS server on the specified port.
func (s *serverImpl) StartServer(port string) {
	log.Fatal(http.ListenAndServeTLS(":"+port, "cert.pem", "key.pem", s.mux))
}

// AddHandler adds a new handler function to the server for the specified path.
func (s *serverImpl) AddHandler(path string, handler http.HandlerFunc) {
	modifiedPath := fmt.Sprint("/%s/%s", s.boundedContext , path)
	s.mux.HandleFunc(modifiedPath, handler)
}
