# 🦠 Plataforma de Identificação de Bactérias Resistentes via HSI

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Backend-FastAPI-blue)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-cyan)
![Docker](https://img.shields.io/badge/Infra-Docker-blueviolet)

Este projeto consiste em uma aplicação web Fullstack para o processamento e análise de **Imagens Hiperespectrais (HSI)** no infravermelho de ondas curtas (SWIR). O objetivo é automatizar o pré-processamento de dados para auxiliar na identificação de bactérias resistentes.

A plataforma realiza leitura de arquivos ENVI, calibração radiométrica, detecção automática de região de interesse (ROI) via Visão Computacional e tratamentos espectrais avançados.

---

## ✨ Funcionalidades

* **Upload de Cubos de Dados:** Suporte para arquivos no formato ENVI (`.raw` e `.hdr`).
* **Calibração Radiométrica Científica:** Correção de reflectância utilizando referências de escuro (*Dark Reference*) e branco (*White Reference*).
* **Detecção Automática de ROI:** Utiliza a **Transformada de Hough** para identificar e isolar automaticamente o batoque (recipiente da amostra) na imagem.
* **Pré-processamento Espectral:**
    * **SNV (Standard Normal Variate):** Para correção de espalhamento de luz.
    * **Filtro Savitzky-Golay:** Para suavização e cálculo da derivada (taxa de variação espectral).
* **Visualização Interativa:** Exibição de previews RGB das amostras e gráficos comparativos (histogramas/espectros médios) antes e depois do processamento.

---

## 🛠️ Tecnologias Utilizadas

### Frontend
* **React** com **TypeScript** (via Vite)
* **Bootstrap** (Interface gráfica responsiva)
* **Axios** (Comunicação com API)

### Backend
* **Python 3.10+**
* **FastAPI** (Servidor API de alta performance)
* **Spectral Python (SPy)** (Manipulação de cubos HSI)
* **OpenCV** (Visão Computacional e Processamento de Imagem)
* **SciPy & NumPy** (Cálculos matemáticos e filtros de sinal)
* **Matplotlib** (Geração de gráficos estáticos)

---

## 📂 Estrutura do Projeto

```text
ProjetoBacteria/
├── backend/                # API e Scripts de Processamento Python
│   ├── main.py             # Servidor FastAPI
│   ├── processing_bridge.py # Orquestrador do pipeline
│   ├── leitura.py          # Leitura ENVI, Calibração e Hough
│   ├── snv.py              # Algoritmo Standard Normal Variate
│   ├── savgol.py           # Algoritmo Savitzky-Golay
│   └── requirements.txt    # Dependências do Python
│
├── frontend/               # Aplicação Web React
│   ├── src/
│   │   ├── pages/Home.tsx  # Interface Principal
│   │   ├── services/api.ts # Conexão com o Backend
│   │   └── ...
│   └── package.json        # Dependências do Node.js
│
└── docker-compose.yml      # (Opcional) Orquestração de containers
🚀 Como Rodar o Projeto
Você precisará de dois terminais abertos (um para o backend e outro para o frontend).

Pré-requisitos
Python 3.10 ou superior

Node.js 18 ou superior

Passo 1: Configurar o Backend (Python)
Acesse a pasta do backend:

Bash

cd backend
Crie um ambiente virtual (opcional, mas recomendado):

Bash

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
Instale as dependências:

Bash

pip install -r requirements.txt
Inicie o servidor:

Bash

python main.py
O servidor rodará em: http://localhost:8000

Passo 2: Configurar o Frontend (React)
Abra um novo terminal e acesse a pasta do frontend:

Bash

cd frontend
Instale as dependências:

Bash

npm install
Inicie a aplicação:

Bash

npm run dev
Acesse a aplicação em: http://localhost:5173

📊 Como Utilizar
Abra a aplicação no navegador.

Na seção de upload, carregue os 6 arquivos obrigatórios para garantir a calibração correta:

Amostra: Arquivos .raw e .hdr da bactéria.

Dark Reference: Arquivos .raw e .hdr da captura no escuro.

White Reference: Arquivos .raw e .hdr da captura na referência branca.

Selecione os filtros desejados (SNV, Savitzky-Golay).

Clique em "Processar e Calibrar".

O sistema retornará:

A visualização do batoque detectado (ROI).

O gráfico do espectro médio calibrado (Antes).

O gráfico do espectro médio processado (Depois).

🐳 Rodando com Docker (Alternativa)
Se você tiver o Docker instalado, pode rodar tudo com um único comando na raiz do projeto:

Bash

docker-compose up --build
A aplicação estará disponível em http://localhost:3000.

📝 Licença
Este projeto foi desenvolvido para fins acadêmicos e de pesquisa científica.

Autor: [Hugo Fonseca Mourao]
