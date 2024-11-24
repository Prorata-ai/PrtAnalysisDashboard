# Proxt so that we can connect to Azure hosted indexing service
# To access it from Cursor, use localhost:8081. To access it from a container, use <fqdn>:8081
# To kill it:
#  ps aux | grep "port-forward" | grep "attribution"
# kill <PID>
kubectl port-forward svc/attribution 8892:8892 -n default

