package k8s

import (
	"fmt"
	"testing"
)

func TestGetConfigMap(t *testing.T) {
	i := NewMockK8sClient().(*MockK8sClient)
	i.CreateConfigMapUsing("test-namespace", "test-configmap", map[string]string{"key": "value"})
	result, err := i.GetConfigMap("test-namespace", "test-configmap")
	fmt.Printf("########### %s \n", result)
	if err != nil {
		t.Fatalf("error getting config map: %v", err)
	}

	// Check the result
	if result["key"] != "value" {
		t.Errorf("expected configmap name to be 'test-configmap', got '%s'", result["key"])
	}
}
