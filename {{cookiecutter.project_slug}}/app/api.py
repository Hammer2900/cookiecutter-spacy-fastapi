# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from collections import defaultdict
import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import spacy
import uvicorn

from app.models import (
    ENT_PROP_MAP,
    RecordsRequest,
    RecordsResponse,
    RecordsEntitiesByTypeResponse,
)

load_dotenv(find_dotenv())
prefix = os.getenv("CLUSTER_ROUTE_PREFIX")
if not prefix:
    prefix = ""
prefix = prefix.rstrip("/")

app = FastAPI(
    title="{{cookiecutter.project_name}}",
    version="1.0",
    description="{{cookiecutter.project_short_description}}",
    openapi_prefix=prefix,
)

# nlp = spacy.load("{{cookiecutter.project_language}}")
nlp = spacy.load("en_core_web_sm")

ENT_PROP_MAP = {
    "CARDINAL": "cardinals",
    "DATE": "dates",
    "EVENT": "events",
    "FAC": "facilities",
    "GPE": "gpes",
    "LANGUAGE": "languages",
    "LAW": "laws",
    "LOC": "locations",
    "MONEY": "money",
    "NORP": "norps",
    "ORDINAL": "ordinals",
    "ORG": "organizations",
    "PERCENT": "percentages",
    "PERSON": "people",
    "PRODUCT": "products",
    "QUANTITY": "quanities",
    "TIME": "times",
    "WORK_OF_ART": "worksOfArt",
}


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"{prefix}/docs")


@app.post("/entities", response_model=RecordsResponse, tags=["NER"])
async def extract_entities(body: RecordsRequest):
    """Extract Named Entities from a batch of Records."""

    res = []
    documents = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    return {"values": res}


@app.post(
    "/entities_by_type", response_model=RecordsEntitiesByTypeResponse, tags=["NER"]
)
async def extract_entities_by_type(body: RecordsRequest):
    """Extract Named Entities from a batch of Records separated by entity label.
        This route can be used directly as a Cognitive Skill in Azure Search
        For Documentation on integration with Azure Search, see here:
        https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface"""

    res = []
    documents = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    res = []

    return {"values": res}
