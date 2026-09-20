# Captcha Solver

Resolve o captcha numérico de 5 dígitos do BHISS Digital usando segmentação por
visão computacional (OpenCV) + template matching vetorizado, sem depender de
nenhum serviço externo de OCR.

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
   -> escala de cinza + median blur (remove ruido "sal e pimenta" do JPEG)
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
   -> load_templates() carrega templates.npz uma unica vez e monta uma
      matriz (N_templates x 600) ja centralizada na media e normalizada (L2)
   -> classificar um recorte e um produto matricial unico (matrix @ vetor)
      contra todos os N templates de uma vez, sem laco por classe
   -> a linha de maior score decide o digito (o rotulo correspondente vem
      do array paralelo `labels`)
        |
4. Concatena os 5 digitos classificados -> string final, ex: "68432"
        |
5. Essa string e o valor pronto pra preencher o campo j_captcha_response
   e submeter a consulta no BHISS Digital
```

Testado em 10 amostras reservadas fora do conjunto de templates (nunca usadas
para gerar ou pré-rotular templates): **100% de acerto por dígito e por
captcha completo**.

### Banco de templates

`templates.npz` é o único artefato que o runtime carrega — um array `crops`
(uint8, 20x30 por recorte) e um array paralelo `labels` (uint8, 0-9),
compactados com `np.savez_compressed`. Hoje tem ~24.700 recortes gerados a
partir de ~5.000 captchas coletados do site.

Não existe mais um diretório `templates/` com um PNG por recorte — essa
representação foi usada durante a fase de curadoria manual (é mais fácil
abrir/mover um arquivo do que editar uma linha de um array), mas uma vez que
o banco estabilizou, o formato de trabalho migrou para o único artefato
binário que o runtime de fato consome. Qualquer correção de rótulo passa a
ser feita em `tools/labels.py` e aplicada com `tools/build_templates.py`.

### Fase de preparação (offline — ver `tools/`)

```
1. tools/collect_samples.py
   -> baixa N imagens de captcha.jpg do site (requisicoes concorrentes)
   -> salva em samples/ (fora do git — ver .gitignore; regeneravel a qualquer
      momento, entao nao ha motivo pra versionar dado bruto)

2. tools/auto_label.py
   -> roda o classificador atual (templates.npz existente) sobre todas as
      amostras de samples/ e grava tools/auto_labels.json com rotulo
      previsto + confianca (score minimo entre os 5 digitos)

3. tools/build_templates.py
   -> decide o rotulo final de cada amostra por ordem de prioridade:
        1. tools/labels.py:VERIFIED_CORRECTIONS  (erro encontrado e corrigido
           manualmente depois do rotulo inicial)
        2. tools/labels.py:SAMPLE_LABELS          (as 40 amostras de treino
           originais, transcritas e conferidas a mao)
        3. auto_label.py, se confianca >= CONFIDENCE_THRESHOLD (0.75)
   -> amostras de HELD_OUT_SAMPLES sao sempre excluidas do banco (sao o
      conjunto de teste)
   -> grava tools/templates.npz -> ../templates.npz

4. tools/evaluate.py
   -> mede a acuracia do classificador contra as 10 amostras de
      HELD_OUT_SAMPLES (nunca usadas para gerar templates)

5. tools/cross_validate.py
   -> treina um classificador "round 1" usando so as 40 amostras de
      TRAIN_SAMPLES (rotulo 100% humano, nunca contaminado por
      auto-rotulagem) e usa ele para re-classificar todas as amostras que
      nao sao treino nem teste
   -> qualquer discordancia entre esse classificador independente e o banco
      de producao vai para tools/disagreements.json, o que reduz uma
      revisão manual de milhares de amostras para dezenas de casos
      suspeitos de fato
   -> tools/build_disagreement_grid.py renderiza esses casos lado a lado com
      a imagem original do captcha (nao so o recorte isolado, que sozinho é
      ambíguo em pares como 1/7, 3/5, 9/0) para decisão rapida
```

Esse pipeline existe porque o banco é majoritariamente auto-rotulado: das
~4.900 amostras usadas hoje, só 40 tiveram rótulo 100% humano desde o início.
Confiar cegamente no auto-rótulo cria risco de autorreforço (um erro vira
template, o template classifica errado de novo, o erro se consolida) — por
isso o corte por confiança e a validação cruzada com um classificador
propositalmente mais fraco e isolado do banco de produção.

## Estrutura

```
captcha_solver/
├── segment_digits.py    # segmentacao: imagem -> 5 recortes de digito
├── classify.py          # classificacao: recorte -> digito (matriz vetorizada)
├── solver.py             # orquestra segment_digits + classify pro runtime
├── templates.npz          # banco de templates (unico artefato versionado)
├── samples/                # captchas brutos coletados (fora do git)
└── tools/                   # scripts de manutencao, nao fazem parte do runtime
    ├── collect_samples.py
    ├── auto_label.py
    ├── build_templates.py
    ├── evaluate.py
    ├── cross_validate.py
    ├── build_review_grid.py
    ├── build_disagreement_grid.py
    └── labels.py
```

## Ampliando o dataset de templates

Se o site mudar a fonte/estilo do captcha, ou a acurácia cair:

1. `tools/collect_samples.py` para coletar mais amostras.
2. `tools/auto_label.py` para pré-rotular usando o classificador atual.
3. `tools/build_templates.py` para reconstruir `templates.npz`.
4. `tools/cross_validate.py` + `tools/build_disagreement_grid.py` para achar
   os poucos casos que valem revisão manual, em vez de revisar tudo.
5. `tools/evaluate.py` antes e depois, pra confirmar que a acurácia no
   conjunto de teste não regrediu.
