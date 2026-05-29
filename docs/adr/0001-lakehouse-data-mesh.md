# ADR 0001: Lakehouse and Data Mesh architecture

## Status
Accepted.

## Context
The Companion product needs operational APIs, batch ingestion, streaming metrics, ML features and embedded analytics with domain ownership.

## Decision
Use S3-compatible object storage as bronze/silver/gold/ml/logs lakehouse zones, Spark with Iceberg-compatible catalog configuration for ELT, Kafka/Flink for streaming, Feast for the feature store, ClickHouse for low-latency serving, Cube.js for the semantic layer and Grafana/frontend for analytics.

## Consequences
The platform can run locally with Docker Compose and can be provisioned in Yandex Cloud via Terraform. Domains publish data products with SLAs and quality metrics.
