# Regulatory AI Backend

A modular backend for regulatory data processing and documentation automation, featuring a FastAPI-based ASGI web server and a LangGraph-powered AI core.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI ASGI server entrypoint
│   └── api/
│       ├── __init__.py
│       └── routes.py         # API route definitions
├── src/
│   └── regulatory/
│       ├── __init__.py       # Project metadata, logger setup
│       ├── agent/            # Agent logic for regulatory tasks
│       │   └── __init__.py
│       ├── chains/           # Chains for GSPR, component recommendation, etc.
│       │   ├── __init__.py
│       │   ├── component_recommender_chain.py
│       │   ├── gspr_filter_chain.py
│       │   └── gspr_generator_chain.py
│       ├── graph/            # Workflow/state graph logic
│       │   ├── __init__.py
│       │   ├── state.py
│       │   └── workflow.py
│       ├── gspr/             # GSPR-specific logic
│       │   └── __init__.py
│       ├── memory/           # (Reserved for memory/state modules)
│       │   └── __init__.py
│       ├── models/           # Data models for GSPR, components, etc.
│       │   ├── __init__.py
│       │   ├── component_recommender_model.py
│       │   ├── gspr_filter_model.py
│       │   └── gspr_generator_model.py
│       ├── prompts/          # Prompt templates for LLMs
│       │   ├── __init__.py
│       │   ├── component_recommender_prompt.py
│       │   ├── gspr_filter_prompt.py
│       │   └── gspr_generator_prompt.py
│       ├── services/         # Service layer (business logic)
│       │   └── __init__.py
│       └── utils/            # Utilities and logging
│           ├── __init__.py
│           ├── helpers.py
│           └── logger.py
├── pyproject.toml
└── README.md
```

---

## Core Features (`src/regulatory/`)

- **Modular AI Backend:**  
  Extensible architecture for regulatory documentation, focused on Design History File (DHF) "Device Input" automation.

- **Chains & Agents:**  
  Implements composable logic for GSPR filtering, component recommendation, and GSPR document generation.

- **Prompt Engineering:**  
  Advanced prompt templates for regulatory compliance (EU MDR, US FDA, Indian MDR).

- **Models:**  
  Typed models for regulatory data, GSPR sections, and component recommendations.

- **Workflow Graphs:**  
  State and workflow management for regulatory processes.

- **Logging & Utilities:**  
  Centralized logging configuration and helper utilities for robust backend operations.

---

## ASGI Web Server (`app/main.py`)

- **FastAPI Application:**  
  Serves as the main entry point, exposing RESTful endpoints for regulatory operations.

- **API Routing:**  
  All endpoints are organized under `app/api/routes.py`.

- **Logging:**  
  Uses a custom logger setup from `src/regulatory/utils/logger.py`.

- **Development & Production Ready:**  
  Run locally with Uvicorn; production deployment supported via Gunicorn/Uvicorn workers.

---



























This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.## License---Contributions are welcome! Please open issues or submit pull requests for enhancements, bug fixes, or new features. Ensure that your code adheres to the existing style and includes appropriate tests.## Contributing---   Visit [http://localhost:8000/docs](http://localhost:8000/docs) after starting the server.3. **Access API docs:**     ```   uvicorn app.main:app --reload   ```bash2. **Run the ASGI server:**   ```   pip install -r requirements.txt   ```bash1. **Install dependencies:**## Getting Started
## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r pyproject.toml
   ```

2. **Run the ASGI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access API docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) after starting the server.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

---

## License

Licensed under the MIT License.