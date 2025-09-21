# Dubai Infrastructure Management Project

This project provides a full-stack solution for managing and analyzing Dubai's infrastructure data, including a React frontend and a Python backend (API + agent tools).

---

## Backend Setup (Python API & Agent)

- Python 3.13 or higher (recommended)
- [pip](https://pip.pypa.io/en/stable/)
- (Optional) [virtualenv](https://virtualenv.pypa.io/en/latest/) for isolated environments
- SQLite3 (for database)


### 2. Create and Activate a Virtual Environment (Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies
```sh
pip install -r requirements.txt
```

### 4. Database Setup(Optional)
- The SQLite database is provided in `data/dubai_infrastructure.db`.
- If you need to regenerate or update data, use the data generator:
```sh
python data/generator.py
```

### 5. Start the Backend API
From the project root directory:
```sh
cd api
uvicorn app:app --reload
```
- The API will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



### 6. Start the Agent (Optional, for CLI interaction)
From the project root directory:
```sh
python agents/infrastructure_agent.py
```


open separate terminal 
## Frontend Setup (React App)

### 1. Prerequisites
- [Node.js](https://nodejs.org/) (v16+ recommended)
- [npm](https://www.npmjs.com/)

### 2. Install Frontend Dependencies
```sh
cd frontend
npm install
```

### 3. Start the Frontend Development Server
```sh
npm start
```
- The app will run at [http://localhost:3000](http://localhost:3000) by default.

### 4. Configuration
- If your backend API is not running on the default port or host, update the API endpoint in the frontend code (see `frontend/src/` for API calls).

---

## Project Structure

- `agents/` — Python agent tools and logic
- `api/` — FastAPI backend
- `data/` — SQLite database and CSVs
- `data_generator/` — Scripts to generate or update data
- `frontend/` — React frontend app
- `requirements.txt` — Python dependencies

---

## Troubleshooting
- Ensure you are in the correct directory when running commands.
- For backend issues, check Python version and virtual environment activation.
- For frontend issues, ensure Node.js and npm are installed and run commands inside the `frontend` folder.
- If you encounter database errors, verify the presence of `data/dubai_infrastructure.db` or regenerate it.

---

## License
Add your license information here.

---

## Contact
For questions or support, contact the project maintainer.
