# MedAI - Medical Drug Interaction Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_AI-FF6B6B?style=for-the-badge&logo=openai&logoColor=white)

**An AI-powered medical analysis platform for drug interactions, food interactions, therapeutic duplication, and symptom checking.**

</div>

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 💊 **Drug-Drug Interaction** | Analyze potential interactions between multiple medications, classified as Major, Moderate, or Minor risk |
| 🍎 **Drug-Food Interaction** | Check for adverse interactions between medications and food items |
| 🔄 **Therapeutic Duplication** | Identify overlapping therapies that may cause adverse effects |
| 🩺 **Symptom Checker** | AI-powered symptom analysis based on user input (symptoms, age, gender, country) |
| 📋 **Drug Details** | Get comprehensive information about specific medications |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Groq AI** - LLM API using Llama 3.3-70b-versatile model
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Next-generation build tool
- **React Router** - Client-side routing
- **Lucide React** - Icon library

---

## 📁 Project Structure

```
med_AI/
├── app.py                 # FastAPI main application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables 
├── menu/
│   ├── drug_interaction/
│   │   ├── drug_drug.py           # Drug-drug interaction module
│   │   ├── drug_food.py           # Drug-food interaction module
│   │   └── therapeutic_duplication.py  # Therapeutic duplication check
│   ├── drug_details/
│   │   └── drug_detail.py         # Drug information module
│   └── symptoms_checker/
│       └── symptom_check.py       # Symptom analysis module
└── frontend/
    ├── src/
    │   ├── pages/                 # React page components
    │   ├── components/            # Reusable UI components
    │   ├── services/              # API service layer
    │   └── styles/                # CSS stylesheets
    └── package.json
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key ([Get one here](https://console.groq.com/))

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/med_AI.git
cd med_AI
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

---

## 🚀 Running the Application

### Start Backend Server
```bash
# From project root
python app.py
# Server runs at http://localhost:8000
```

### Start Frontend Development Server
```bash
cd frontend
npm run dev
# Frontend runs at http://localhost:5173
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
PORT=8000
GROQ_API_KEY=your_groq_api_key_here
```

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Backend server port (default: 8000) | No |
| `GROQ_API_KEY` | Your Groq API key for LLM access | **Yes** |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/aggregate_interactions` | Analyze drug-drug, drug-food interactions & therapeutic duplications |
| `POST` | `/drug_details` | Get detailed information about medications |
| `POST` | `/drug_drug` | Check drug-drug interactions only |
| `POST` | `/symptom_check` | AI-powered symptom analysis |
| `GET` | `/health` | Health check endpoint |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns.

---

<div align="center">
Made with ❤️ for better healthcare decisions
</div>
