# Proxt so that we can connect to Azure hosted indexing service
# To access it from Cursor, use localhost:8081. To access it from a container, use <fqdn>:8081
kubectl port-forward svc/recommender-service 8896:8896 -n default

