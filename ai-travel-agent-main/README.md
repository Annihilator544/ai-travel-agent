# ✈️🧳 AI Travel Agent - VoyageVerse Prototype

This repository is a prototype for VoyageVerse — a unified AI-driven travel
platform that integrates LLM orchestration, flight/hotel search, itinerary
generation, real-time checks, and a small recommender scaffold.

## Quickstart (local)

1. Create and activate a virtual environment (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install runtime and dev dependencies:
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Copy `.env.example` to `.env` and fill in keys (see below).

4. Run tests using the provided runner:
```powershell
python run_tests.py
```

## Environment variables & GitHub Actions secrets

The project uses a number of third-party APIs. Add these environment variables
locally or as GitHub repository secrets (Settings → Secrets & variables → Actions):

- `SENDGRID_API_KEY` — SendGrid API key for email sending (optional).
- `FROM_EMAIL`, `TO_EMAIL`, `EMAIL_SUBJECT` — Email metadata used by the agent.
- `OPENAI_API_KEY` — LLM provider credentials if using OpenAI/ChatOpenAI.
- `SERPAPI_API_KEY` — SerpAPI key used by flights/hotels tools.
- `WEATHER_API_KEY` or `OPENWEATHER_API_KEY` — OpenWeatherMap API key for weather tool.
- `AVIATIONSTACK_API_KEY` — AviationStack API key for flight status tool (optional).

**Security note:** Do NOT commit secrets. Use GitHub Secrets for CI and `.env` locally.

## Replacing stubs with production integrations

- `agents/tools/weather.py` — uses OpenWeatherMap when `WEATHER_API_KEY` is set; otherwise returns a safe stub.
- `agents/tools/flight_status.py` — uses AviationStack when `AVIATIONSTACK_API_KEY` is set; otherwise returns a safe stub.
- `agents/itinerary/itinerary_builder.py` — illustrates a multi-step itinerary assembly; expand with LLM-driven composition.

## CI and testing

- GitHub Actions workflow at `.github/workflows/ci.yml` runs compile checks, the custom test runner, and flake8 linting.
- Local tests can be run with `python run_tests.py` if you don't want to install pytest.

## Next steps (recommended)

1. Add persistent user behavior storage (MongoDB or similar) and pipeline for the recommender.
2. Implement a production-grade forecasting model for dynamic pricing (Prophet/LSTM) and replace `agents/pricing/price_forecast.py`.
3. Prototype a federated learning workflow (TensorFlow Federated) for privacy-preserving personalization.

If you'd like, I can implement any of the above — tell me which one to prioritize and I'll add a plan and scaffold.

---
Generated edits updated the repository to better align with the VoyageVerse project report.

## Federated learning simulation (local)

The repository includes a lightweight Federated Averaging (FedAvg) simulation
under `agents/federated/` that demonstrates the protocol without requiring
TensorFlow Federated. It is intended for educational and prototyping use.

Run the simulation locally:
```powershell
# from project root
python -c "import sys; sys.path.insert(0, 'ai-travel-agent-main'); from agents.federated.run_fed import main; main()"
```

This will print a sample trained model weight vector. For production-ready FL
you should migrate this scaffold to TensorFlow Federated or PySyft and
implement secure aggregation and client orchestration.

