from fastapi import FastAPI,Form, Request
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import re
from embed import tokenizer, model, tokenize_and_generate_embeddings
import uuid
import numpy
from pinecone import Pinecone
import json
import os
from dotenv import load_dotenv
load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


index_name = "url-query"
index = pc.Index(index_name)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers


@app.get("/",)
def root(url:str, query: str):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    for meta_tag in soup.find_all("meta"):
        meta_tag.decompose()

# 2. Remove all <style> and <script> tags
    for style_tag in soup.find_all("style"):
        style_tag.decompose()

    for script_tag in soup.find_all("script"):
        script_tag.decompose()

# 3. Remove inline styles and classes from <div> and other elements
    for div in soup.find_all("div"):
        div.attrs.pop("style", None)  # Remove inline style
        div.attrs.pop("class", None)  # Remove class attribute

# 4. Optionally, you can also remove the id attribute if not needed
    for div in soup.find_all("div"):
        div.attrs.pop("id", None)
    text_tags = {'p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a', 'strong', 'em'}
    for i, div in enumerate(soup.find_all("div"), start=1):
        has_text_tag = any(child.name in text_tags for child in div.descendants if getattr(child, 'name', None))
        if(has_text_tag):
            embeddings =  tokenize_and_generate_embeddings(div.text, tokenizer, model,max_tokens=500)
            upsert= []
            for  embedding in embeddings:
                data = {
                    "id": str(uuid.uuid4()), 
            "values": embedding[0].cpu().numpy().flatten(), 
            "metadata": {"dom":str(div)[:1000], "text":str(embedding[1]+"")}
        }
                upsert.append(data)
            index.upsert(upsert)
    eb = tokenize_and_generate_embeddings(query, tokenizer, model)
    query_vector = eb[0][0].cpu().numpy().flatten().astype(numpy.float32).tolist()
    response = index.query(
        vector=query_vector,
        top_k=10,
        include_metadata=True,
        include_values=False
        )
    return json.dumps([{"dom":i['metadata']['dom'], "score":i["score"],"text":i['metadata']['text']}  for i in response["matches"] if "text" in i['metadata'].keys() ])