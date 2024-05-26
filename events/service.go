package events

// EventPayload represents the payload of an event.
type EventPayload struct {
	Data      string `json:"data"`
	CreatedAt int64  `json:"created_at"`
	Version   int    `json:"version"`
}

// Event represents an event.
type Event struct {
	Id            int64             `json:"id"`
	SourceContext string            `json:"source_context"`
	Payload       EventPayload      `json:"payload"`
	Tags          map[string]string `json:"tags"`
}
