

## Distance (original version)

```bash
docker buildx build --platform linux/amd64 -t registry.fabvision.it/lookup-distance-ferrara-amd64:latest --push .
```


## Distance (new version)

Faccio il build localmente:

```bash
docker buildx build --platform linux/amd64 -f Dockerfile2 -t registry.fabvision.it/lookup-distance2-ferrara-amd64:latest --push .
```

Sul server:

# Crea la cartella se non esiste
mkdir -p ~/lookup-fe-distance2

# Esegui il container con i volumi montati
docker run -d \
  --name lookup-distance2-service \
  -p 5002:5002 \
  --env-file .env.lookup-distance-ferrara \
  -v ~/lookup-fe-distance2:/app/shared \
  registry.fabvision.it/lookup-distance2-ferrara-amd64:latest



```bash
docker pull registry.fabvision.it/lookup-distance2-ferrara-amd64:latest
docker rm -f lookup-distance2-ferrara

docker run -p 5002:5002 -v /root/lookup-fe-distance2:/app/shared --env-file .env.lookup-distance-ferrara --detach --restart always --name lookup-distance2-ferrara registry.fabvision.it/lookup-distance2-ferrara-amd64:latest
```

```bash
docker exec -it lookup-distance2-ferrara bash

docker run -p 5002:5002 -v /root/lookup-fe-distance2:/app/shared --env-file .env.lookup-distance-ferrara --detach --restart always --name lookup-distance2-ferrara registry.fabvision.it/lookup-distance2-ferrara-amd64:latest

docker stop lookup-distance2-ferrara
docker rm lookup-distance2-ferrara
```





cestino

  -v ~/lookup-fe-distance2/distance_cache.json:/app/distance_cache.json \
  -v ~/lookup-fe-distance2/points_of_interest.json:/app/points_of_interest.json \
