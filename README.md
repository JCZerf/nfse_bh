# NFS-e BH

Automação para consulta e validação de Notas Fiscais de Serviço Eletrônicas
(NFS-e) emitidas pela Prefeitura de Belo Horizonte através do portal
[BHISS Digital](https://bhissdigital.pbh.gov.br/nfse). Dado o CNPJ do
prestador, o número da nota e o código de verificação, a API resolve o
captcha do site sozinha, consulta a nota, baixa o XML oficial (assinado
digitalmente) e devolve tudo já estruturado.

## Como funciona

```
Cliente --(POST /nfse/validation)--> API (FastAPI)
                                        |
                                        v
                              bot.bhiss_collector
                    (sessao + ViewState + submit do form)
                                        |
                                        v
                              captcha_solver.solve
                (segmentacao OpenCV + template matching)
                                        |
                                        v
                              XML oficial da nota (ABRASF)
                                        |
                                        v
                              bot.nfse_extractor
                    (XPath no XML, seletor no HTML)
                                        |
                                        v
                              resposta estruturada + XML em base64
```

Nenhuma etapa depende de navegador (Playwright/Selenium) ou de serviço de
OCR de terceiros — a consulta inteira roda com `httpx` async e o captcha é
resolvido localmente.

## Destaques técnicos

- **Captcha resolvido sem OCR de terceiros**: segmentação por visão
  computacional (OpenCV) + template matching vetorizado (numpy/BLAS).
  100% de acerto no conjunto de teste reservado, ~4ms por captcha. Detalhes
  em [`captcha_solver/README.md`](captcha_solver/README.md).
- **Sessão JSF reversa manualmente**: o portal usa RichFaces/JSF com
  `ViewState` dinâmico por sessão — descoberto via engenharia reversa do
  fluxo real do site, sem depender de nenhum SDK oficial.
- **Fonte de dados dupla**: os campos são extraídos do XML oficial
  (assinado, padrão ABRASF) sempre que possível, com fallback pro HTML da
  página só para os textos descritivos que o XML não traz (ex: descrição do
  item de serviço).

## Estrutura do projeto

```
main.py                        # cria o FastAPI() e inclui os routers
api/
├── routes/nfse.py              # POST /nfse/validation
├── services/nfse_service.py    # orquestra collector -> solver -> extractor
├── models/nfse.py               # contratos Pydantic de request/response
└── dependencies/auth.py         # autenticacao por X-API-Key
bot/
├── bhiss_collector.py           # cliente httpx async do BHISS Digital
├── nfse_data.py                  # schema da NFS-e (path XML/HTML por campo)
└── nfse_extractor.py             # popula o schema a partir do XML + HTML
captcha_solver/                   # modulo de resolucao de captcha (ver seu README)
tests/                             # suite pytest (fixtures com dados sinteticos)
```

## Requisitos

- Python 3.13+

## Instalação

```bash
pip install -e .
```

Para rodar os testes, instale também o grupo `dev`:

```bash
pip install -e ".[dev]"
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com a chave de API que os
clientes deverão enviar no header `X-API-Key`:

```
API_KEY=uma-chave-secreta-qualquer
```

## Rodando a API

```bash
uvicorn main:app --reload
```

### Exemplo de uso

```bash
curl -X POST http://localhost:8000/nfse/validation \
  -H "Content-Type: application/json" \
  -H "X-API-Key: uma-chave-secreta-qualquer" \
  -d '{
    "provider_cnpj": "21.150.875/0001-40",
    "nfse_number": "202000000010823",
    "verification_code": "a1dd4050"
  }'
```

Resposta (resumida):

```json
{
  "metadata": {
    "request_id": "aedf0070",
    "timestamp": "2026-09-19T22:43:40.702380Z",
    "source_data": {
      "fields": [
        { "name": "nfse_number", "origin": "xml", "value": "202000000010823" },
        { "name": "service_item_description", "origin": "html", "value": "Agenciamento, organizacao..." }
      ],
      "xml_base64": "..."
    }
  }
}
```

## Testes

```bash
pytest
```
