# MFL AI Security Lab — START HERE
**Author:** @freyley.leyva

Laboratorio educativo 100% ficticio para el XI Simposio de Software Libre y Código Abierto de la Mixteca 2026.

## Misión
BUILD → BREAK → DEFEND → PROVE.

## Requisitos
- Git
- Docker Desktop
- Visual Studio Code
- 8 GB RAM mínimo recomendado (16 GB mejora la experiencia con modelos locales)

## 1. Explora antes de ejecutar
```powershell
cd MFL_AI_Security_Lab_v0.1
dir
code .
```

## 2. Levanta la arquitectura
```powershell
docker compose up -d
docker compose ps
```

## 3. Descarga los modelos (primera vez)
```powershell
docker compose exec ollama ollama pull qwen2.5:1.5b
docker compose exec ollama ollama pull nomic-embed-text
```

## 4. Abre MFL
- Frontend: http://localhost:8501
- API/Swagger: http://localhost:8000/docs
- Qdrant: http://localhost:6333/dashboard
- Jaeger: http://localhost:16686

## 5. Ingesta los documentos ficticios
Desde Swagger usa `POST /ingest`, o PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/ingest"
```

## 6. Pregunta
Usa la interfaz web. El objetivo inicial no es memorizar comandos: es entender el flujo.

> Todo el contenido, identidades, políticas y datos del laboratorio son ficticios. No uses datos, secretos, credenciales o arquitectura de una organización real.
