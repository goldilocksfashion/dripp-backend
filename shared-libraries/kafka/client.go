// shared-libraries/kafka/client.go
package kafka

import (
	"shared-libraries/k8s"
	"sync"

	ckafka "github.com/confluentinc/confluent-kafka-go/kafka"
)

// Consumer that consumes from topics by subscribing to them.
type Consumer interface {
	Subscribe(topic string) error
	Receive() (string, error)
	Close() error
}

// Producer that sends messages to topics.
type Producer interface {
	Send(topic string, message string) error
	Close() error
}

// Client that connects to a Kafka cluster and provides consumers and producers.
type Client interface {
	Start() error
	Close() error
}

// DefaultClient default implementation of Client.
type DefaultClient struct {
	k8sInstance k8s.K8sClient
	c           *ckafka.Consumer
	p           *ckafka.Producer
	config      *ckafka.ConfigMap
}

var instance *DefaultClient
var once sync.Once

// GetInstance gets the singleton instance of the DefaultClient.
func GetInstance() Client {
	once.Do(func() {
		configMap, err := k8s.GetInstance().GetConfigMap("kafka", "config")
		if err != nil {
			panic(err)
		}
		ckafkaConfig := &ckafka.ConfigMap{
			"bootstrap.servers": configMap["bootstrap.servers"],
		}
		instance = &DefaultClient{config: ckafkaConfig}
	})
	return instance
}

// shared-libraries/kafka/client.go
func (c *DefaultClient) Start() error {
	consumer, err := ckafka.NewConsumer(c.config)
	if err != nil {
		return err
	}
	producer, err := ckafka.NewProducer(c.config)
	if err != nil {
		return err
	}
	c.c = consumer
	c.p = producer
	return nil
}

// shared-libraries/kafka/client.go
func (c *DefaultClient) Close() error {
	c.c.Close()
	c.p.Close()
	return nil
}
