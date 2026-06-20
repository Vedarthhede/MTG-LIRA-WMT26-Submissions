
# WMT 2026 Low-Resource Indic MT

This repository contains training configurations and preprocessing utilities used for developing Neural Machine Translation (NMT) systems for the WMT 2026 Shared Task on Low-Resource Indic Languages using OpenNMT-py.

## Contents

### Training Configurations

* `assamese.yaml` – English–Assamese model configuration
* `bodo.yaml` – English–Bodo model configuration
* `mizo.yaml` – English–Mizo model configuration
* `multilingual_joint_finetuning.yaml` – Multilingual fine-tuning setup (english to indic)
* `reverse-multilingual_joint_finetuning.yaml` – Multilingual fine-tuning setup (indic to english)
* 
### Preprocessing Utilities

* `datacleaner.py` – Parallel corpus cleaning and filtering
* `indiannormalizer.py` – Indian language text normalization
* `langinfo.py` – Language metadata and script information
* `normalizercode.py` – Core normalization functions

## Framework

* OpenNMT-py, Eole
* Transformer Architecture
* SentencePiece Tokenization
* PyTorch

## Workflow

Raw Data → Normalization → Cleaning → Tokenization → Vocabulary Creation → Training → Evaluation

## Usage
Tokenization:

Train a model:

```bash
onmt_train -config assamese.yaml
```

## Research Context

These configurations were developed for experiments in:

* Low-Resource Machine Translation
* Multilingual Transfer Learning
* Indic Language Processing
* WMT 2026 Shared Task Systems

## License

Released for research and educational purposes.

