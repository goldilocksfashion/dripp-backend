package kafka

// Message represents a generic Kafka message
type Message struct {
	Topic string
	Key   string
	Value []byte
}

// Producer defines the interface for a Kafka producer
type Producer interface {
	Produce(msg Message) error
	Close()
}

// Consumer defines the interface for a Kafka consumer
type Consumer interface {
	Subscribe(topics []string) error
	ReadMessage() (*Message, error)
	Close()
}
