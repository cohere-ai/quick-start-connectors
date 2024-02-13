import json
import logging
import requests
from flask import current_app as app
from dictdot import dictdot

logger = logging.getLogger(__name__)

START_SNIPPET = "<%START%>"
END_SNIPPET = "<%END%>"


def _remove_snippet(s: str) -> str:
    return s.replace(START_SNIPPET, "").replace(END_SNIPPET, "")


def send_request(config: dict, data: dict) -> dict:
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
    return result


def vectara_query(
    query: str,
    config: dict,
) -> None:
    """Query Vectara and return the results.
    Args:
        query: query string
    """
    config.corpus_id = config.corpus_id.split(",")
    corpus_key = [
        {
            "customerId": config.customer_id,
            "corpusId": config.corpus_id[i],
            "lexicalInterpolationConfig": {"lambda": config.lambda_val},
        }
        for i in range(len(config.corpus_id))
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

    result = send_request(config, data)

    responses = result["responseSet"][0]["response"]
    documents = result["responseSet"][0]["document"]

    error_codes = [
        "BAD_REQUEST",
        "UNAUTHORIZED",
        "FORBIDDEN",
        "NOT_FOUND",
        "METHOD_NOT_ALLOWED",
        "CONFLICT",
        "UNSUPPORTED_MEDIA_TYPE",
        "TOO_MANY_REQUESTS",
        "INTERNAL_SERVER_ERROR",
        "NOT_IMPLEMENTED",
        "SERVICE_UNAVAILABLE",
        "INSUFFICIENT_STORAGE",
    ]

    status_list = result["responseSet"][0]["status"]
    if len(status_list) > 0 and status_list[0]["code"] in error_codes:
        logger.error("Query failed: %s", result)
        return []

    res = []
    for resp in responses[: config.similarity_top_k]:
        md = {m["name"]: m["value"] for m in resp["metadata"]}
        doc_inx = resp["documentIndex"]
        doc_id = documents[doc_inx]["id"]
        doc_md = {m["name"]: m["value"] for m in documents[doc_inx]["metadata"]}
        item = {"id": doc_id, "text": _remove_snippet(resp["text"])}
        item.update(doc_md)
        item.update(md)
        res.append(item)

    return res


def search(query):
    assert (apikey := app.config.get("API_KEY")), "VECTARA_API_KEY env var must be set"

    assert (
        customer_id := app.config.get("CUSTOMER_ID")
    ), "VECTARA_CUSTOMER_ID env var must be set"

    assert (
        corpus_id := app.config.get("CORPUS_ID")
    ), "VECTARA_CORPUS_ID env var must be set"

    config = dictdot(
        {
            "api_key": str(apikey),
            "customer_id": str(customer_id),
            "corpus_id": str(corpus_id),
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
    )

    results = vectara_query(query, config)
    return results
