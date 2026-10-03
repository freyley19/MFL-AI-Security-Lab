# =========================================================
# MFL Bank — AI Security Lab
# Author: @freyley.leyva
# BUILD → BREAK → DEFEND → PROVE
# =========================================================

.PHONY: help up status ingest warmup prove down

help:
	@echo ""
	@echo "🏦 MFL Bank — AI Security Lab"
	@echo "============================="
	@echo ""
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  make up       Levanta el laboratorio"
	@echo "  make status   Muestra el estado de los servicios"
	@echo "  make ingest   Ingresa documentos a la Knowledge Base"
	@echo "  make warmup   Inicializa el modelo local"
	@echo "  make prove    Ejecuta las pruebas de seguridad"
	@echo "  make down     Apaga el laboratorio"
	@echo ""

up:
	@echo ""
	@echo "🚀 MFL — START"
	@echo "Levantando servicios..."
	@docker compose up -d
	@echo ""
	@docker compose ps

status:
	@echo ""
	@echo "📊 MFL — STATUS"
	@docker compose ps

ingest:
	@echo ""
	@echo "📚 MFL — INGEST"
	@echo "Construyendo Knowledge Base..."
	@curl -s -X POST http://localhost:8000/ingest
	@echo ""

warmup:
	@echo ""
	@echo "🔥 MFL — WARMUP"
	@echo "Inicializando modelo local..."
	@curl -s -X POST http://localhost:8000/warmup
	@echo ""

prove:
	@echo ""
	@echo "🟣 MFL — PROVE"
	@echo "Preparando security regression tests..."
	@docker compose cp tests/security_tests.py api:/tmp/security_tests.py
	@docker compose exec api python /tmp/security_tests.py

down:
	@echo ""
	@echo "🛑 MFL — STOP"
	@docker compose down