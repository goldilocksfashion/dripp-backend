package kafka

import (
	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"testing"
)

type MockProducer struct {
	mock.Mock
}

func (m *MockProducer) Produce(topic string, message []byte) error {
	args := m.Called(topic, message)
	return args.Error(0)
}

type MockConsumer struct {
	mock.Mock
}

func (m *MockConsumer) ReadMessage() (*kafka.Message, error) {
	args := m.Called()
	return args.Get(0).(*kafka.Message), args.Error(1)
}

func TestProduceMessage(t *testing.T) {
	mockProducer := new(MockProducer)
	mockProducer.On("Produce", "test-topic", []byte("hello world")).Return(nil)

	err := mockProducer.Produce("test-topic", []byte("hello world"))
	assert.NoError(t, err)
	mockProducer.AssertExpectations(t) // Verify that the expected interactions occurred.
}
