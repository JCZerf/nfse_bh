from prometheus_client import Counter, Histogram

nfse_queries_total = Counter(
    "nfse_queries_total",
    "Total de consultas de NFS-e realizadas",
    ["status"],
)

nfse_query_duration_seconds = Histogram(
    "nfse_query_duration_seconds",
    "Duracao da consulta de NFS-e em segundos",
)
