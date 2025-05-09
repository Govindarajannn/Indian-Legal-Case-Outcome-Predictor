# 🧑‍⚖️ Indian Supreme Court Case Outcome Predictor

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/downloads/release/python-310/)
[![Model](https://img.shields.io/badge/Model-LLaMA3.1--8B-orange)]()
[![Vector DB](https://img.shields.io/badge/VectorDB-Qdrant-purple)](https://qdrant.tech/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This project builds a **domain-adapted, fine-tuned LLM** to **predict outcomes of Supreme Court cases in India**, using **real legal texts from 2023–2024**. It combines web scraping, case summarization, retrieval-augmented generation (RAG), continuous pretraining, fine-tuning, and robust evaluation to build a specialized legal reasoning model.

---

## 📌 Project Overview

| Step | Description |
|------|-------------|
| 🔗 **Data Extraction** | Scraped Supreme Court case links and case texts from [Indian Kanoon](https://www.indiankanoon.org/) |
| 📝 **Case Summarization** | Summarized cases into structured sections using a local LLaMA3.1-8B model |
| ⚖️ **Law Retrieval (RAG)** | Retrieved relevant Indian Penal Code laws using vector search (Qdrant) |
| 🔄 **Pretraining & Fine-tuning** | Domain-adapted the LLM and trained it to predict judgments |
| 📊 **Evaluation** | Evaluated predictions using faithfulness, ROUGE, BLEU, and BERT-based metrics |

---

## 📂 Directory Structure

```bash
.
├── links.py
├── case-extraction.py
├── data-preprocessing.ipynb
├── rag.ipynb
├── pretraining+finetuning.ipynb
├── evaluation.ipynb
├── data/
│   ├── 2024_cases/
│   └── 2023_cases/
└── models/
    └── llama3.1-8b/
```

---

## 🏛️ Data Source

- **Website**: [Indian Kanoon](https://www.indiankanoon.org/)
- **Court**: Supreme Court of India
- **Training Data**: Cases from 2024
- **Testing Data**: Cases from 2023

---

## 🧠 Model Architecture

- **Base Model**: LLaMA 3.1 8B
- **Techniques**:
  - Summarization into `FACTS`, `ARGUMENTS`, `OBSERVATIONS`, `JUDGMENT`
  - Retrieval-Augmented Generation (RAG) with IPC
  - Instruction–Input–Output formatting
  - Continuous pretraining and task-specific fine-tuning

---

## 🔍 Evaluation Metrics & Results

| Metric                  | Score     |
|-------------------------|-----------|
| **Faithfulness**        | 0.7064    |
| **ROUGE-1**             | 0.4797    |
| **ROUGE-2**             | 0.2797    |
| **ROUGE-L**             | 0.3613    |
| **BLEU**                | 0.2139    |
| **BERTScore**           | 0.8862    |
| **Sentence-BERT Cosine**| 0.7064    |

> 📈 These scores indicate strong semantic and factual alignment with true outcomes.

---

## 🛠️ Technologies Used

- 🐍 Python 3.10+
- 🦙 LLaMA 3.1–8B (local inference)
- 💾 Qdrant (vector DB)
- 📄 PyPDF (for IPC PDF parsing)
- 🤗 HuggingFace metrics: ROUGE, BLEU, BERTScore, Sentence-BERT

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/indian-case-outcome-predictor.git
cd indian-case-outcome-predictor

# Install dependencies
pip install -r requirements.txt

# Run steps
python links.py
python case-extraction.py

# Run notebooks in order
1. data-preprocessing.ipynb
2. rag.ipynb
3. pretraining+finetuning.ipynb
4. evaluation.ipynb
```

---

## 🧪 Example Output Format

```json
{
  "instruction": "Predict the outcome of the case.",
  "input": "[Summarized case text + relevant IPC sections]",
  "output": "Appeal Dismissed"
}
```

---

## 📌 Future Work

- Support more courts (High Courts, Tribunals)
- Legal precedent tracing & citation support
- Web interface for legal researchers

---

## 📄 License

This project is licensed under the MIT License.