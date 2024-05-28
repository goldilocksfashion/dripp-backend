package vectordb

import (
	"context"
	"log"
	sharedlibraries "shared-libraries"
	"shared-libraries/k8s"
	"sync"

	"github.com/milvus-io/milvus-sdk-go/v2/client"
)

type Vector struct {
	ID     string
	Vector []float64
}

type VectorDbClient interface {
	GetVector(ctx context.Context, id string) (*Vector, error)
	PutVector(ctx context.Context, vector *Vector) error
	DeleteVector(ctx context.Context, id string) error
}

type VectorDbClientImpl struct {
	milvusClient *client.Client
}

var once sync.Once
var instance VectorDbClient

func GetInstance() VectorDbClient {
	once.Do(func() {
		instance = newVectorDbClient()
	})
	return instance
}
func (c VectorDbClientImpl) GetVector(ctx context.Context, id string) (*Vector, error) {
	return nil, nil
}
func (c VectorDbClientImpl) PutVector(ctx context.Context, vector *Vector) error {
	return nil
}
func (c VectorDbClientImpl) DeleteVector(ctx context.Context, id string) error {
	return nil
}

func newVectorDbClient() VectorDbClient {
	k8sClient := k8s.GetInstance()
	conf, err := k8sClient.GetConfigMap(string(sharedlibraries.DefaultNamespace), string(sharedlibraries.DefaultFeatureDbConfig))
	if err != nil {
		log.Fatal("failed to get config map:", err.Error())
	}

	milvusClient, err := client.NewGrpcClient(
		context.Background(),                      // ctx
		conf[string(sharedlibraries.UrlVectorDb)], // addr
	)
	if err != nil {
		log.Fatal("failed to connect to Milvus:", err.Error())
	}
	return VectorDbClientImpl{
		milvusClient: &milvusClient,
	}
}
