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

captcha_result_total = Counter(
    "captcha_result_total",
    "Resultado do captcha conforme aceito ou rejeitado pela fonte",
    ["result"],
)

captcha_solve_duration_seconds = Histogram(
    "captcha_solve_duration_seconds",
    "Duracao da resolucao do captcha em segundos",
    buckets=(0.001, 0.002, 0.003, 0.005, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0),
)
