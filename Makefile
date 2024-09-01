.PHONY: up
up:
	@docker compose -f docker-compose.yaml up -d


.PHONY: stop
stop:
	@docker compose -f docker-compose.yaml stop

.PHONY: logs
logs:
	@docker compose -f docker-compose.yaml logs -f