### Pipeline Orchestration & Automation

This pipeline is orchestrated using Prefect and runs on a scheduled basis.

Key features:
- Incremental ingestion using the latest available date per metric
- Automatic retries on transient failures
- Full pipeline observability stored in PostgreSQL (`pipeline_runs`)
- Safe re-runs with idempotent upserts

The pipeline is scheduled to run daily and logs both successful and failed executions.
