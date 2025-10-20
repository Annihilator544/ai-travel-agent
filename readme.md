# ✈️🧳 AI Travel Agent - VoyageVerse Prototype

This repository is a prototype for VoyageVerse — a unified AI-driven travel
platform that integrates LLM orchestration, flight/hotel search, itinerary
generation, real-time checks, and a small recommender scaffold.

## Project Structure

```
Travel Agent/
├── .venv/                          # Virtual environment (created in setup)
├── ai-travel-agent-main/           # Main project directory
│   ├── agents/                     # Agent modules
│   │   ├── federated/              # Federated learning simulation
│   │   ├── itinerary/              # Itinerary generation
│   │   ├── pricing/                # Dynamic pricing
│   │   ├── recommender/            # Recommendation system
│   │   ├── tools/                  # API integration tools
│   │   └── ...
│   ├── tests/                      # Test suite
│   ├── requirements.txt            # Runtime dependencies
│   ├── requirements-dev.txt        # Development dependencies
│   └── README.md                   # Detailed project documentation
└── run_fed_local.py                # Convenience script to run federated learning
```

## Quickstart (Local Setup)

### 1. Create and activate virtual environment

From the **base directory** (`Travel Agent/`):

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install runtime dependencies
pip install -r ai-travel-agent-main\requirements.txt

# Install development dependencies
pip install -r ai-travel-agent-main\requirements-dev.txt
```

### 3. Configure environment variables

Copy the example environment file and fill in your API keys:

```powershell
cd ai-travel-agent-main
copy .env.example .env
# Edit .env with your API keys
cd ..
```

### 4. Run tests

```powershell
cd ai-travel-agent-main
python run_tests.py
cd ..
```

### 5. Run federated learning simulation

```powershell
# From base directory (Travel Agent/)
python run_fed_local.py
```

## Environment Variables & API Keys

The project uses third-party APIs. Add these to `ai-travel-agent-main\.env`:

- `SENDGRID_API_KEY` — SendGrid API key for email sending (optional)
- `FROM_EMAIL`, `TO_EMAIL`, `EMAIL_SUBJECT` — Email metadata
- `OPENAI_API_KEY` — OpenAI/ChatGPT API credentials
- `SERPAPI_API_KEY` — SerpAPI key for flights/hotels search
- `WEATHER_API_KEY` or `OPENWEATHER_API_KEY` — OpenWeatherMap API key
- `AVIATIONSTACK_API_KEY` — AviationStack API for flight status (optional)

**Security note:** Never commit your `.env` file or API keys to version control.

## Available Scripts

### `run_fed_local.py`
Runs the federated learning simulation from the base directory.

```powershell
python run_fed_local.py
```

### Running tests
Navigate to the project directory and run the test suite:

```powershell
cd ai-travel-agent-main
python run_tests.py
```

### Direct federated learning execution
Alternative way to run the simulation:

```powershell
cd ai-travel-agent-main
python -c "from agents.federated.run_fed import main; main()"
cd ..
```

## Troubleshooting

### Dependency Conflicts
If you encounter package conflicts, try:

```powershell
# Uninstall conflicting packages
pip uninstall langchain langchain-openai langchain-core numpy -y

# Reinstall from requirements
pip install -r ai-travel-agent-main\requirements.txt
```

### NumPy Import Errors
If you see NumPy C-extension errors:

```powershell
pip uninstall numpy -y
pip install numpy
```

### Path Issues
Ensure you're running scripts from the correct directory:
- `run_fed_local.py` — run from **base directory** (`Travel Agent/`)
- `run_tests.py` — run from **project directory** (`ai-travel-agent-main/`)

## Features

- **LLM Orchestration**: LangChain-based agent for travel planning
- **Flight & Hotel Search**: SerpAPI integration for real-time availability
- **Itinerary Generation**: Multi-step travel plan assembly
- **Dynamic Pricing**: Price forecasting scaffold
- **Federated Learning**: Privacy-preserving personalization simulation
- **Real-time Updates**: Weather and flight status checks
- **Email Integration**: SendGrid-powered notifications

## Next Steps

1. **Persistent Storage**: Add MongoDB for user behavior tracking
2. **Advanced Pricing**: Implement Prophet/LSTM for price forecasting
3. **Production FL**: Migrate to TensorFlow Federated or PySyft
4. **Enhanced Security**: Implement differential privacy mechanisms
5. **API Gateway**: Add FastAPI endpoints for web integration

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- Syntax checks
- Test suite execution
- Flake8 linting

## License

See project documentation for licensing details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python run_tests.py`
5. Submit a pull request

---

For detailed technical documentation, see `ai-travel-agent-main/README.md`