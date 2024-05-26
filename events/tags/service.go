package eventtagmanagement

import (
	"shared-libraries/kafka"
	"strconv"
	"time"
)


// EventTagManager tags eventsn based on bounded context and event types
type EventTagManager interface {
	TagEvent(event *Event) error
}

// EventTagManagerImpl is the default implementation of EventTagManager.
type EventTagManagerImpl struct {
	kafkClient kafka.Client
}

// NewEventTagManager creates a new EventTagManager.
func NewEventTagManager(kafkaClient *kafka.Client) EventTagManager {
	instance := kafka.GetInstance()
	err := instance.Start()
	if err != nil {
		panic(err)
	}
	return &EventTagManagerImpl{kafkClient: instance}
}

// TagEvent tags an event with a tag.
func (e *EventTagManagerImpl) TagEvent(event *Event) error {
	event.Tags["source_context"] = event.SourceContext
	event.Tags["created_at"] = strconv.FormatInt(event.Payload.CreatedAt, 10)
	event.Tags["id"] = strconv.FormatInt(event.Id, 10)
	event.Tags["tagged_at"] = strconv.FormatInt(time.Now().Unix(), 10)
	err := e.kafkClient.Send(event.SourceContext, event.Payload.Data)
	if err != nil {
		return err
	}
	return nil
}
