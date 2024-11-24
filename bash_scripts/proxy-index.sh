# Proxt so that we can connect to Azure hosted indexing service
# To access it from Cursor, use localhost:8081. To access it from a container, use <fqdn>:8081
# To kill it:
# ps aux | grep "port-forward" | grep "indexing-search-api"
# kill <pid>
kubectl port-forward svc/indexing-search-api 8081:8081 -n default

