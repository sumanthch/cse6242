#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import traceback
import pickle

app = FastAPI()

# Set up CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS","GET","POST"],
    allow_headers=["*"],
)

model_ame = pickle.load(open('/code/models/AME_model.pkl', 'rb'))
model_asia = pickle.load(open('/code/models/Asia_model.pkl', 'rb'))
model_eu = pickle.load(open('/code/models/EU_model.pkl', 'rb'))
model_na = pickle.load(open('/code/models/NA_model.pkl', 'rb'))
model_sa = pickle.load(open('/code/models/SA_model.pkl', 'rb'))
model_wu = pickle.load(open('/code/models/WU_model.pkl', 'rb'))

# model_ame = pickle.load(open('models/AME_model.pkl', 'rb'))
# model_asia = pickle.load(open('models/Asia_model.pkl', 'rb'))
# model_eu = pickle.load(open('models/EU_model.pkl', 'rb'))
# model_na = pickle.load(open('models/NA_model.pkl', 'rb'))
# model_sa = pickle.load(open('models/SA_model.pkl', 'rb'))
# model_wu = pickle.load(open('models/WU_model.pkl', 'rb'))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
def predict(data: Dict):
    
	assert isinstance(data, dict)
	try:
		if "features" in data.keys():
			probs = {"Africa/Middle East": model_ame.predict_proba([data['features']])[0][1],
					"Asia": model_asia.predict_proba([data['features']])[0][1],
					"Eastern Europe": model_eu.predict_proba([data['features']])[0][1],
					"North America": model_na.predict_proba([data['features']])[0][1],
					"South America": model_sa.predict_proba([data['features']])[0][1],
					"Western Europe": model_wu.predict_proba([data['features']])[0][1]
					}
			print(probs)
		else:
			raise KeyError('The input should be a dict with features as a key')
		
		return JSONResponse(content=probs)

	except Exception:
		response_json = {"status_code": 404,  "error": "exception", "trace": traceback.format_exc()}
		return JSONResponse(content=response_json)
