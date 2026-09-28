# Troubleshooting — MFL
**Author:** @freyley.leyva

## `no configuration file provided`
Ejecuta `docker compose` desde la carpeta donde está `compose.yaml`.

## PowerShell: `curl -X` falla
En Windows PowerShell, `curl` puede ser alias de `Invoke-WebRequest`. Usa:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/ingest"
```

## Ver estado
```powershell
docker compose ps
```

## Ver logs
```powershell
docker compose logs -f api
```

## Ollama aún no tiene modelos
```powershell
docker compose exec ollama ollama pull qwen2.5:1.5b
docker compose exec ollama ollama pull nomic-embed-text
```
