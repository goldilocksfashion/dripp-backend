package kafka

import "github.com/confluentinc/confluent-kafka-go/v2/kafka"

type DrippEventProducer struct {
	P *kafka.Producer
}

// NewProducer creates a new Kafka producer
func NewProducer(brokers string) (*DrippEventProducer, error) {
	p, err := kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": brokers})
	if err != nil {
		return nil, err
	}
	return &DrippEventProducer{P: p}, nil
}

// Produce sends a message to the Kafka topic
func (p *DrippEventProducer) Produce(msg Message) error {
	return p.P.Produce(&kafka.Message{
		TopicPartition: kafka.TopicPartition{Topic: &msg.Topic, Partition: kafka.PartitionAny},
		Key:            []byte(msg.Key),
		Value:          msg.Value,
	}, nil)
}

// Close closes the producer client
func (p *DrippEventProducer) Close() {
	p.P.Close()
}
