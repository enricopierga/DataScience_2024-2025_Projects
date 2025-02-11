# Chatbot

## Quick startup guide

> **Note:** This project uses Python 3.10

### 0. Clone the repository

```bash
git clone https://github.com/enricopierga/fitBot_rasa
cd fitBot_rasa
```

## 1. Activate the conda project

```bash
conda activate Rasa_es_310
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or:

```bash
pip3.10 install -r requirements.txt
```

### 3. Train the model

```bash
cd rasa
rasa train
```

### 4. Start the action server

```bash
cd rasa
rasa run actions
```

### 5. Start the chatbot in CLI

In a different terminal:

```bash
rasa shell
```
