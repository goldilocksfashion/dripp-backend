package schema

import (
    "testing"

    "github.com/golang/mock/gomock"
    "github.com/stretchr/testify/assert"
)

func TestGetSchema(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRegistry := mock_schema.NewMockSchemaRegistryInterface(ctrl)

    expectedSchema := schema.EventSchema{ID: 1, SourceContext: "test", Version: 1}
    mockRegistry.EXPECT().GetSchema("test", 1).Return(expectedSchema, nil)

    // Replace with the actual function you're testing, which should use the mock
    actualSchema, err := YourFunctionThatUsesSchemaRegistry(mockRegistry, "test", 1)

    assert.NoError(t, err)
    assert.Equal(t, expectedSchema, actualSchema)
}

func TestGetLatestSchema(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRegistry := mock_schema.NewMockSchemaRegistryInterface(ctrl)

    expectedSchema := schema.EventSchema{ID: 1, SourceContext: "test", Version: 1}
    mockRegistry.EXPECT().GetLatestSchema("test").Return(expectedSchema, nil)
    assert.Equal(t, expectedSchema, actualSchema)
}