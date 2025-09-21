from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')  # Ensure parent dir is in path for imports
from agents.infrastructure_agent import (
	agent,
	query_infrastructure_by_district,
	get_critical_alerts,
	get_infrastructure_stats_by_risk,
	get_infrastructure_stats_by_district
)

app = FastAPI()

# Add CORS middleware for frontend compatibility
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # You can restrict this to ["http://localhost:3000"] for more security
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

# Pydantic model for agent query
from pydantic import BaseModel

class AgentQueryRequest(BaseModel):
	query: str


@app.post('/agent/query')
async def agent_query(body: AgentQueryRequest):
	user_input = body.query
	if not user_input:
		raise HTTPException(status_code=400, detail='Missing query')
	try:
		response = agent(user_input)
		msg = response.message
		import json
		text_content = None
		# Always try to extract only the 'text' field from the response
		def extract_text(obj):
			if isinstance(obj, dict):
				if 'text' in obj:
					return obj['text']
				if 'content' in obj and isinstance(obj['content'], list):
					for item in obj['content']:
						if isinstance(item, dict) and 'text' in item:
							return item['text']
			elif isinstance(obj, list):
				for item in obj:
					result = extract_text(item)
					if result:
						return result
			return None

		# Try parsing if string
		if isinstance(msg, str):
			try:
				parsed = json.loads(msg.replace("'", '"'))
				text_content = extract_text(parsed)
			except Exception:
				pass
		else:
			text_content = extract_text(msg)

		if not text_content:
			text_content = str(msg)
		return { 'response': text_content }
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@app.get('/infrastructure')
def infrastructure_by_district(
	district: str = Query('all'),
	risk: str = Query('all')
):
	try:
		result = query_infrastructure_by_district(district, risk)
		return { 'result': result }
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@app.get('/alerts')
def critical_alerts(
	risk: str = Query('critical')
):
	try:
		result = get_critical_alerts(risk)
		return { 'result': result }
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@app.get('/stats/risk')
def stats_by_risk():
	try:
		result = get_infrastructure_stats_by_risk()
		return { 'result': result }
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@app.get('/stats/district')
def stats_by_district():
	try:
		result = get_infrastructure_stats_by_district()
		return { 'result': result }
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
