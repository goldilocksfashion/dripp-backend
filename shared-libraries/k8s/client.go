package k8s

import (
	"context"
	"sync"

	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	fake "k8s.io/client-go/kubernetes/fake"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

// K8sClient k8s client that can get config maps.
type K8sClient interface {
	CreateClient() (K8sClient, error)
	CreateConfigMapUsing(namespace, name string, data map[string]string) error
	GetConfigMap(namespace, name string) (map[string]string, error)
}

type MockK8sClient struct {
	client *fake.Clientset
}

// DefaultK8sClient default implementation of K8sClient.
type DefaultK8sClient struct {
	client *kubernetes.Clientset
}

var instance *DefaultK8sClient
var once sync.Once

func NewMockK8sClient() K8sClient {
	clientset := fake.NewSimpleClientset()
	return &MockK8sClient{client: clientset}
}

func (m *MockK8sClient) CreateConfigMapUsing(namespace, name string, data map[string]string) error {
	configMap := &v1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name: name,
		},
		Data: data,
	}
	_, err := m.client.CoreV1().ConfigMaps(namespace).Create(context.TODO(), configMap, metav1.CreateOptions{})
	return err
}

func (m *MockK8sClient) GetConfigMap(namespace, name string) (map[string]string, error) {
	configMap, err := m.client.CoreV1().ConfigMaps(namespace).Get(context.TODO(), name, metav1.GetOptions{})
	if err != nil {
		return nil, err
	}
	return configMap.Data, nil
}

func (m *MockK8sClient) CreateClient() (K8sClient, error) {
	return m, nil
}
func (m *MockK8sClient) GetClient() *fake.Clientset {
	return m.client
}
func (m *MockK8sClient) SetClient(client *fake.Clientset) {
	m.client = client
}
func (m *MockK8sClient) SetConfigMap(namespace, name string, data map[string]string) error {
	configMap := &v1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name: name,
		},
		Data: data,
	}
	_, err := m.client.CoreV1().ConfigMaps(namespace).Create(context.TODO(), configMap, metav1.CreateOptions{})
	return err
}
func (m *MockK8sClient) GetConfigMapData(namespace, name string) (map[string]string, error) {
	configMap, err := m.client.CoreV1().ConfigMaps(namespace).Get(context.TODO(), name, metav1.GetOptions{})
	if err != nil {
		return nil, err
	}
	return configMap.Data, nil
}

func (m *MockK8sClient) CreateConfigMap(namespace, name string, data map[string]string) error {
	configMap := &v1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name: name,
		},
		Data: data,
	}
	_, err := m.client.CoreV1().ConfigMaps(namespace).Create(context.TODO(), configMap, metav1.CreateOptions{})
	return err
}

// GetInstance gets the instance of the DefaultK8sClient.
func GetInstance() K8sClient {
	once.Do(func() {
		instance = &DefaultK8sClient{}
	})
	return instance
}

// NewK8sClient creates a new K8sClient.
func (d *DefaultK8sClient) CreateConfigMapUsing(namespace, name string, data map[string]string) error {
	configMap := &v1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name: name,
		},
		Data: data,
	}
	_, err := d.client.CoreV1().ConfigMaps(namespace).Create(context.TODO(), configMap, metav1.CreateOptions{})
	return err
}

// GetConfigMap gets a config map from a namespace.
func (d *DefaultK8sClient) GetConfigMap(namespace, name string) (map[string]string, error) {
	configMap, err := d.client.CoreV1().ConfigMaps(namespace).Get(context.TODO(), name, metav1.GetOptions{})
	if err != nil {
		return nil, err
	}
	return configMap.Data, nil
}

// NewK8sClient creates a new K8sClient.
func (d *DefaultK8sClient) CreateClient() (K8sClient, error) {
	// Load the in-cluster config if available, otherwise load the local config
	config, err := rest.InClusterConfig()
	if err != nil {
		config, err = clientcmd.BuildConfigFromFlags("", clientcmd.RecommendedHomeFile)
		if err != nil {
			return nil, err
		}
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, err
	}
	return &DefaultK8sClient{client: clientset}, nil
}
