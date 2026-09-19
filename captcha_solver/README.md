# Captcha Solver

Resolve o captcha numérico de 5 dígitos do BHISS Digital usando segmentação por
visão computacional (OpenCV) + template matching, sem depender de nenhum
serviço externo de OCR.

## Como funciona

O captcha do site é sempre uma sequência de 5 dígitos, fundo em gradiente liso
(sem ruído/blur), fonte branca em negrito. Isso permite resolver com correlação
de templates em vez de um modelo de OCR genérico.

### Fase de uso real (runtime)

Fluxo que o restante do sistema (`bot/bhiss_collector.py`) chama:

```
1. Recebe a imagem crua do captcha (bytes, baixada via httpx)
        |
2. segment_digits.segment_image()
   -> escala de cinza + median blur (remove ruido "sal e pimenta")
   -> binariza por brilho (branco = digito, preto = fundo)
   -> fecha pequenas quebras morfologicamente (ex: "0" partido em 2 pedacos)
   -> detecta componentes conectados (blobs brancos)
   -> filtra o artefato fixo de borda (barra decorativa do captcha)
   -> garante exatamente 5 digitos:
        - excesso de componentes (digitos colados)  -> funde os mais proximos
        - falta de componentes (digitos grudados)    -> separa pelo "vale"
          de menor densidade de pixels
   -> recorta e normaliza cada digito pro mesmo tamanho (20x30)
        |
3. classify.classify_digit() - para cada um dos 5 recortes
   -> compara (cv2.matchTemplate, correlacao normalizada) contra todos os
      templates de cada uma das 10 classes (0-9) em templates/
   -> escolhe a classe cujo melhor template teve maior score
        |
4. Concatena os 5 digitos classificados -> string final, ex: "68432"
        |
5. Essa string é o valor pronto pra preencher o campo j_captcha_response
   e submeter a consulta no BHISS Digital
```

Testado em 10 amostras reservadas fora do conjunto de templates: **100% de
acerto por dígito e por captcha completo**.

### Fase de preparação (offline, já executada — ver `tools/`)

```
1. tools/collect_samples.py
   -> baixa N imagens de captcha.jpg do site (requisicoes concorrentes)
   -> salva em samples/

2. segment_digits.py rodado sobre cada amostra de samples/
   -> mesmo pipeline de segmentacao descrito acima

3. tools/auto_label.py
   -> roda o classificador atual sobre as amostras novas para pre-rotula-las

4. tools/build_templates.py
   -> usa os rotulos confirmados manualmente (tools/labels.py) para as
      amostras de treino originais, e as predicoes do auto_label.py para
      o restante
   -> agrupa os recortes resultantes em templates/0/, templates/1/, ...,
      templates/9/

5. tools/evaluate.py
   -> mede a acuracia do classificador contra as amostras de teste
      reservadas em tools/labels.py (nunca usadas para gerar templates)
```

## Estrutura

```
captcha_solver/
├── segment_digits.py   # segmentacao: imagem -> 5 recortes de digito
├── classify.py         # classificacao: recorte -> digito (template matching)
├── templates/           # banco de templates, um subdiretorio por digito (0-9)
├── samples/              # captchas brutos coletados (para expandir o dataset)
└── tools/                # scripts de manutencao, nao fazem parte do runtime
    ├── collect_samples.py
    ├── build_templates.py
    ├── auto_label.py
    ├── evaluate.py
    ├── labels.py
    └── build_review_grid.py
```

## Ampliando o dataset de templates

Se o site mudar a fonte/estilo do captcha, ou a acurácia cair, repita a fase
de preparação: `tools/collect_samples.py` para coletar mais amostras,
`tools/auto_label.py` para pré-rotular usando o classificador atual, revisar
os casos duvidosos, e `tools/build_templates.py` para reconstruir o banco de
templates.
