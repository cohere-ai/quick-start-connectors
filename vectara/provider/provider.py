import json
import logging
import requests
from flask import current_app as app

logger = logging.getLogger(__name__)

START_SNIPPET = "<%START%>"
END_SNIPPET = "<%END%>"

def remove_snippet(s: str) -> str:
    return s.replace(START_SNIPPET, "").replace(END_SNIPPET, "")

def vectara_query(
    query: str,
    config: dict,
) -> None:
    """Query Vectara and return the results.
    Args:
        query: query string
    """
    config.vectara_corpus_id = config.vectara_corpus_id.split(',')
    corpus_key = [
        {
            "customerId": config.vectara_customer_id,
            "corpusId": config.corpus_id[i],
            "lexicalInterpolationConfig": {"lambda": config.lambda_val},
        }
        for i in range(len(config.vectara_corpus_id))
    ]
    if len(config.filter) > 0:
        for k in corpus_key:
            k["metadataFilter"] = config.filter

    data = {
        "query": [
            {
                "query": query,
                "start": 0,
                "numResults": config.mmr_k if config.mmr else config.similarity_top_k,
                "contextConfig": {
                    "sentencesBefore": config.n_sentences_before,
                    "sentencesAfter": config.n_sentences_after,
                    "startTag": START_SNIPPET,
                    "endTag": END_SNIPPET,
                },
                "corpusKey": corpus_key,
            }
        ]
    }
    if config.mmr:
        data["query"][0]["rerankingConfig"] = {
            "rerankerId": 272725718,
            "mmrConfig": {"diversityBias": config.mmr_diversity_bias},
        }

    headers = {
        "x-api-key": config.api_key,
        "customer-id": config.customer_id,
        "Content-Type": "application/json",
        "X-Source": "cohere-connect",
    }


    response = requests.post(
        headers=headers,
        url="https://api.vectara.io/v1/query",
        data=json.dumps(data),
        timeout=config.timeout,
    )

    if response.status_code != 200:
        logger.error(
            "Query failed %s",
            f"(code {response.status_code}, reason {response.reason}, details "
            f"{response.text})",
        )
        return []

    result = response.json()

    responses = result["responseSet"][0]["response"]
    documents = result["responseSet"][0]["document"]

    metadatas = []
    for x in responses:
        md = {m["name"]: m["value"] for m in x["metadata"]}
        doc_num = x["documentIndex"]
        doc_md = {m["name"]: m["value"] for m in documents[doc_num]["metadata"]}
        md.update(doc_md)
        metadatas.append(md)

    res = []
    for x in responses:
        md = {m["name"]: m["value"] for m in x["metadata"]}
        doc_inx = x["documentIndex"]
        doc_id = documents[doc_inx]["id"]
        doc_md = {m["name"]: m["value"] for m in documents[doc_num]["metadata"]}
        item = {
            "id": doc_id,
            "text": remove_snippet(x["text"])
        }
        item.update(doc_md)
        item.update(md)
        res.append(item)

    return res

def search(query):
    assert (
        apikey := app.config.get("VECTARA_API_KEY")
    ), "VECTARA_API_KEY env var must be set"

    assert (
        customer_id := app.config.get("VECTARA_CUSTOMER_ID")
    ), "VECTARA_CUSTOMER_ID env var must be set"

    assert (
        corpus_id := app.config.get("VECTARA_CORPUS_ID")
    ), "VECTARA_CORPUS_ID env var must be set"

    config = {
        "api_key": apikey,
        "customer_id": customer_id,
        "corpus_id": corpus_id,
        "lambda_val": 0.025,
        "filter": "",
        "similarity_top_k": 10,
        "mmr": True,
        "mmr_k": 50,
        "mmr_diversity_bias": 0.3,
        "n_sentences_before": 2,
        "n_sentences_after": 2,
        "timeout": 120,
    }

    results = vectara_query(query, config)
    return results
