# Sistema Híbrido de Reconhecimento Facial

##  Visão Geral

Este sistema combina **face_recognition** e **DeepFace** em uma estratégia híbrida inteligente que otimiza tanto velocidade quanto precisão no reconhecimento facial.

##  Resultados da Comparação

Baseado em testes com 429 imagens de celebridades:

| Modelo | Acurácia | Velocidade Média | F1 Score | Precisão | Recall |
|--------|----------|------------------|----------|----------|--------|
| **face_recognition** | 77.6% | ~0.09s | 0.84 | 0.86 | 0.82 |
| **DeepFace (Facenet)** | 54.1% | ~1.7s | 0.68 | 0.74 | 0.63 |

##  Estratégias Disponíveis

### 1. SMART (Recomendado) 

Estratégia inteligente que adapta o processamento baseado na confiança:

```
1. Executa face_recognition (rápido)
2. Se confiança >= 60%: 
    Aceita resultado imediatamente
3. Se confiança entre 40-60%:
    Valida com DeepFace
    Aceita se ambos concordam
4. Se confiança < 40%:
    Usa DeepFace como autoridade
5. Se não encontrar:
    Tenta DeepFace como fallback
```

**Vantagens:**
-  Rápido na maioria dos casos (~90%)
-  Alta precisão quando necessário
-  Melhor custo-benefício
-  Ideal para sistemas de presença

**Tempo médio:** ~0.3s (mix de casos rápidos e validados)

### 2. ALWAYS_BOTH (Máxima Precisão)

Sempre executa ambos os modelos e combina resultados:

```
1. Executa face_recognition
2. Executa DeepFace
3. Compara resultados:
   - Se concordam: aceita com alta confiança
   - Se discordam: usa o de maior confiança
```

**Vantagens:**
-  Máxima precisão
-  Reduz falsos positivos
-  Ideal para aplicações críticas

**Desvantagens:**
-  Sempre mais lento (~1.8s)
-  Maior custo computacional

### 3. FALLBACK (Máxima Velocidade)

Usa face_recognition, DeepFace apenas em falhas:

```
1. Executa face_recognition
2. Se encontrar: aceita
3. Se não encontrar: tenta DeepFace
```

**Vantagens:**
-  Mais rápido possível
-  Fallback para casos difíceis

**Desvantagens:**
-  Pode ter falsos positivos
-  Menos validação

##  Como Usar

### Reconhecimento Padrão (SMART)

```python
POST /faces/reconhecer
Content-Type: multipart/form-data

foto: [arquivo de imagem]
mode: "smart"  # opcional, default
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "message": "Chamada registrada para João Silva!",
  "student_id": "123",
  "nome": "João Silva",
  "confidence": 87.5,
  "recognition_details": {
    "student_id": "123",
    "confidence": 87.5,
    "method_used": "face_recognition_only",
    "processing_time": 0.095,
    "agreement": null,
    "details": {
      "face_recognition": {
        "student_id": "123",
        "confidence": 87.5
      },
      "deepface": null
    }
  }
}
```

### Teste Comparativo

```python
POST /faces/reconhecer/teste
Content-Type: multipart/form-data

foto: [arquivo de imagem]
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Teste de reconhecimento concluído",
  "results": {
    "smart": {
      "student_id": "123",
      "confidence": 87.5,
      "method_used": "face_recognition_only",
      "processing_time": 0.095,
      "student_name": "João Silva"
    },
    "always_both": {
      "student_id": "123",
      "confidence": 85.2,
      "method_used": "both_agree",
      "processing_time": 1.823,
      "agreement": true,
      "student_name": "João Silva"
    },
    "fallback": {
      "student_id": "123",
      "confidence": 87.5,
      "method_used": "face_recognition_only",
      "processing_time": 0.093,
      "student_name": "João Silva"
    }
  },
  "recommendation": "SMART mode recomendado - ambos modelos concordam com alta confiança"
}
```

## 📈 Métricas de Desempenho

### Tipos de Resultado (method_used)

- `face_recognition_only`: FR de alta confiança, aceito diretamente
- `hybrid_validated`: FR + DF concordam
- `face_recognition_priority`: FR e DF discordam, FR escolhido
- `deepface_priority`: FR baixa confiança, DF escolhido
- `deepface_fallback`: FR não encontrou, DF encontrou
- `face_recognition_unvalidated`: DF não confirmou FR
- `both_agree`: Modo always_both com concordância
- `both_no_match`: Nenhum encontrou
- `both_uncertain`: Ambos inseguros

### Agreement (Concordância)

- `true`: Ambos os modelos concordam no ID
- `false`: Modelos discordam
- `null`: Apenas um modelo foi usado

##  Configuração

### Thresholds de Confiança

Em `app/services/hybrid_face_service.py`:

```python
HIGH_CONFIDENCE_THRESHOLD = 60.0  # Aceita FR direto
LOW_CONFIDENCE_THRESHOLD = 40.0   # Usa DF como autoridade
```

### Tolerância face_recognition

Em `app/services/face_service.py`:

```python
FACE_RECOGNITION_TOLERANCE = 0.6
```

### Configurações DeepFace

Em `app/services/deepface_service.py`:

```python
DEEPFACE_MODEL = "Facenet"
DEEPFACE_DETECTOR = "opencv"
DEEPFACE_DISTANCE_METRIC = "cosine"
```

##  Casos de Uso

### Sistema de Presença (SMART)
- Velocidade + precisão
- Validação em casos duvidosos
- Registro automático de chamada

### Controle de Acesso (ALWAYS_BOTH)
- Máxima segurança
- Dupla validação
- Zero falsos positivos aceitáveis

### Identificação Rápida (FALLBACK)
- Velocidade máxima
- Grande volume de pessoas
- Ambiente controlado

##  Exemplo de Estatísticas

Após 100 reconhecimentos em modo SMART:

```python
{
  "total_recognitions": 100,
  "average_time": 0.287,
  "methods_distribution": {
    "face_recognition_only": "67.0%",
    "hybrid_validated": "21.0%",
    "deepface_fallback": "8.0%",
    "both_no_match": "4.0%"
  },
  "agreement_rate": "21.0%",
  "disagreement_rate": "2.0%"
}
```

**Interpretação:**
- 67% casos resolvidos rapidamente (alta confiança)
- 21% casos validados (concordância)
- 8% casos salvos pelo fallback
- 4% não reconhecidos
- Apenas 2% de discordância

##  Debug e Logging

O sistema imprime logs detalhados no console:

```
 Iniciando reconhecimento com face_recognition...
 face_recognition encontrou: 123 (confiança: 87.50%)
 Alta confiança (87.50%), aceitando resultado
```

```
 Iniciando reconhecimento com face_recognition...
 face_recognition encontrou: 123 (confiança: 52.30%)
 Confiança média (52.30%), validando com DeepFace...
 Ambos concordam! ID: 123
```

##  Notas Importantes

1. **Primeiro Reconhecimento**: O DeepFace pode demorar mais na primeira execução (carregamento de modelos)
2. **Memória**: DeepFace usa mais RAM (~1GB para Facenet)
3. **CPU vs GPU**: DeepFace se beneficia de GPU, mas funciona em CPU
4. **Imagens**: Melhor qualidade = melhor resultado (mínimo 300x300px recomendado)

##  Troubleshooting

### DeepFace não funciona
```bash
# Reinstalar dependências
pip install deepface==0.0.93
pip install tf-keras==2.16.0
```

### Muito lento
- Considere usar modo `fallback`
- Reduzir qualidade das imagens
- Aumentar `HIGH_CONFIDENCE_THRESHOLD`

### Muitos falsos positivos
- Usar modo `always_both`
- Reduzir `FACE_RECOGNITION_TOLERANCE`
- Aumentar qualidade das imagens de cadastro

## 📚 Documentação Adicional

- [Comparação Completa](./tests/comparison_results/README.md)
- [Guia Rápido](./tests/comparison_results/QUICKSTART.md)
- [Estrutura do Projeto](./tests/comparison_results/STRUCTURE.md)

---

**Desenvolvido com ❤ para otimizar reconhecimento facial**
