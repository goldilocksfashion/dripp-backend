package kafka

import "github.com/confluentinc/confluent-kafka-go/v2/kafka"

// DrippEventConsumer  reads kafka topic its subscribed to.
type DrippEventConsumer struct {
	C *kafka.Consumer
}

// NewConsumer creates a new Kafka consumer
func NewConsumer(brokers, groupID string) (*DrippEventConsumer, error) {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": brokers,
		"group.id":          groupID,
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		return nil, err
	}
	return &DrippEventConsumer{C: c}, nil
}

// Subscribe subscribes the consumer to a list of topics
func (c *DrippEventConsumer) Subscribe(topics []string) error {
	return c.C.SubscribeTopics(topics, nil)
}

// ReadMessage reads messages from Kafka
func (c *DrippEventConsumer) ReadMessage() (*Message, error) {
	msg, err := c.C.ReadMessage(-1)
	if err != nil {
		return nil, err
	}
	return &Message{
		Topic: *msg.TopicPartition.Topic,
		Key:   string(msg.Key),
		Value: msg.Value,
	}, nil
}

// Close closes the consumer client
func (c *DrippEventConsumer) Close() {
	err := c.C.Close()
	if err != nil {
		panic(err)
	}
}
