package sharedlibraries

type DrippConstant string

type DrippConfigMapLookupKey string

const (
	DefaultNamespace       DrippConstant           = "dripp-ai-infrastructure"
	DefaultVectorDbConfig  DrippConstant           = "vectordb-config"
	DefaultFeatureDbConfig DrippConstant           = "featuredb-config"
	UrlVectorDb            DrippConfigMapLookupKey = "URL_DB"
)
