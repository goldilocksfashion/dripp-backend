package mock_schema

import (
        reflect "reflect"
        schema "schema"

        gomock "go.uber.org/mock/gomock"
)

// MockSchemaRegistryInterface is a mock of SchemaRegistryInterface interface.
type MockSchemaRegistryInterface struct {
        ctrl     *gomock.Controller
        recorder *MockSchemaRegistryInterfaceMockRecorder
}

// MockSchemaRegistryInterfaceMockRecorder is the mock recorder for MockSchemaRegistryInterface.
type MockSchemaRegistryInterfaceMockRecorder struct {
        mock *MockSchemaRegistryInterface
}

// NewMockSchemaRegistryInterface creates a new mock instance.
func NewMockSchemaRegistryInterface(ctrl *gomock.Controller) *MockSchemaRegistryInterface {
        mock := &MockSchemaRegistryInterface{ctrl: ctrl}
        mock.recorder = &MockSchemaRegistryInterfaceMockRecorder{mock}
        return mock
}

// EXPECT returns an object that allows the caller to indicate expected use.
func (m *MockSchemaRegistryInterface) EXPECT() *MockSchemaRegistryInterfaceMockRecorder {
        return m.recorder
}

// GetLatestSchema mocks base method.
func (m *MockSchemaRegistryInterface) GetLatestSchema(sourceContext string) (schema.EventSchema, error) {
        m.ctrl.T.Helper()
        ret := m.ctrl.Call(m, "GetLatestSchema", sourceContext)
        ret0, _ := ret[0].(schema.EventSchema)
        ret1, _ := ret[1].(error)
        return ret0, ret1
}

// GetLatestSchema indicates an expected call of GetLatestSchema.
func (mr *MockSchemaRegistryInterfaceMockRecorder) GetLatestSchema(sourceContext any) *gomock.Call {
        mr.mock.ctrl.T.Helper()
        return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "GetLatestSchema", reflect.TypeOf((*MockSchemaRegistryInterface)(nil).GetLatestSchema), sourceContext)
}

// GetSchema mocks base method.
func (m *MockSchemaRegistryInterface) GetSchema(sourceContext string, version int) (schema.EventSchema, error) {
        m.ctrl.T.Helper()
        ret := m.ctrl.Call(m, "GetSchema", sourceContext, version)
        ret0, _ := ret[0].(schema.EventSchema)
        ret1, _ := ret[1].(error)
        return ret0, ret1
}

// GetSchema indicates an expected call of GetSchema.
func (mr *MockSchemaRegistryInterfaceMockRecorder) GetSchema(sourceContext, version any) *gomock.Call {
        mr.mock.ctrl.T.Helper()
        return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "GetSchema", reflect.TypeOf((*MockSchemaRegistryInterface)(nil).GetSchema), sourceContext, version)
}