# 🤖 XYZ Company AI Chatbot

A company-specific AI chatbot powered by a fine-tuned language model and Retrieval-Augmented Generation (RAG). The chatbot answers questions accurately about XYZ Company using a fine-tuned model hosted on Hugging Face and Pinecone as the vector database.

---

## 📁 Project Structure

```
├── Company Overview.txt        # Source data about XYZ Company (used for training & RAG)
├── upserting_data.ipynb        # Chunks company data and upserts it into Pinecone
├── FineTune.ipynb              # Fine-tunes the base LLM on company data
├── lora_company_model.zip      # Compressed fine-tuned LoRA model weights
├── ngrok-setup.ipynb           # Hosts the Hugging Face model via ngrok on Kaggle
├── main.py                     # Main application entry point
├── model.py                    # Model loading and inference logic
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🧠 How It Works

Here's the end-to-end flow of how this project was built and how it runs:

```
Company Overview.txt
      │
      ├──► upserting_data.ipynb ──► Pinecone (Vector DB for RAG)
      │
      └──► FineTune.ipynb ──► lora_company_model.zip ──► Hugging Face Hub
                                                                │
                                        ngrok-setup.ipynb ◄────┘
                                               │
                                         Public ngrok URL
                                               │
                                         main.py + model.py
                                               │
                                         🤖 Chatbot (RAG + Fine-tuned Model)
```

---

## ⚙️ Setup Guide

Follow these steps in order to reproduce the project from scratch.

### Prerequisites

- Python 3.9+
- A [Pinecone](https://www.pinecone.io/) account and API key
- A [Hugging Face](https://huggingface.co/) account and token
- A [Kaggle](https://www.kaggle.com/) account (for model hosting)
- A [ngrok](https://ngrok.com/) account and auth token

---

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 2 — Prepare & Upload Company Data to Pinecone

Open and run **`upserting_data.ipynb`**.

This notebook:
- Reads `Company Overview.txt`
- Chunks the text into smaller segments
- Generates embeddings for each chunk
- Upserts all vectors into a Pinecone index

Before running, set your credentials:

```python
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_ENV     = "your-pinecone-environment"
INDEX_NAME       = "your-index-name"
```

---

### Step 3 — Fine-Tune the Model

Open and run **`FineTune.ipynb`**.

This notebook:
- Loads a base LLM
- Applies LoRA (Low-Rank Adaptation) fine-tuning on the company data
- Saves the fine-tuned weights as `lora_company_model.zip`

After fine-tuning:
1. Download `lora_company_model.zip`
2. Push the model to your Hugging Face Hub repository:

```python
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path="./lora_company_model",
    repo_id="your-username/your-model-name",
    repo_type="model"
)
```

---

### Step 4 — Host the Model via ngrok on Kaggle

Open **`ngrok-setup.ipynb`** on [Kaggle](https://www.kaggle.com/) with GPU enabled.

This notebook:
- Loads your fine-tuned model from Hugging Face Hub
- Starts a local inference server
- Exposes it publicly using ngrok

Set your tokens inside the notebook:

```python
HF_TOKEN    = "your-huggingface-token"
NGROK_TOKEN = "your-ngrok-auth-token"
MODEL_NAME  = "your-username/your-model-name"
```

Once running, ngrok will output a **public URL** like:
```
https://xxxx-xx-xx-xxx-xx.ngrok-free.app
```

> ⚠️ **Keep this Kaggle notebook running** throughout the entire session — it hosts the model. Copy the ngrok URL for the next step.

---

### Step 5 — Run the Chatbot

Update the ngrok URL in your environment or config, then start the app:

```bash
python main.py
```

The chatbot will:
- Accept user questions
- Retrieve relevant context from Pinecone (RAG)
- Send the query + context to the hosted fine-tuned model
- Return an accurate, company-specific answer

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENV=your-pinecone-environment
PINECONE_INDEX=your-index-name
HF_TOKEN=your-huggingface-token
NGROK_URL=https://xxxx-xx-xx.ngrok-free.app
```

---

## 📌 Key Design Decisions

| Feature | Choice | Reason |
|---|---|---|
| Fine-tuning method | LoRA | Efficient, lightweight adaptation without full retraining |
| Vector DB | Pinecone | Managed, scalable, fast similarity search |
| Model hosting | Kaggle + ngrok | Free GPU access for inference |
| Retrieval | RAG | Improves answer accuracy with grounded context |

---

## 📝 Notes

- The `lora_company_model.zip` file contains only the LoRA adapter weights, not the full base model.
- The ngrok URL **changes every session** — update it in your `.env` each time you restart the Kaggle notebook.
- `Company Overview.txt` is AI-generated sample company data used as the knowledge base.

---

## 🙌 Acknowledgements

- [Hugging Face](https://huggingface.co/) for model hosting and the `transformers` / `peft` libraries
- [Pinecone](https://www.pinecone.io/) for vector storage
- [ngrok](https://ngrok.com/) for tunneling
- [Kaggle](https://www.kaggle.com/) for free GPU notebooks
