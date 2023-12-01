**Quick Start Connectors**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![](https://img.shields.io/badge/PRs-Welcome-red)

---

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
  - [Features](#features)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

# Overview

Cohere's Build-Your-Own-Connector framework allows you to integrate Cohere's Command LLM via the [co.chat api endpoint](https://docs.cohere.com/reference/chat) to any datastore/software that holds text information and has a corresponding search endpoint exposed in its API. This allows the Commanad model to generated responses to user queries that are grounded in proprietary information.

Some examples of the use-cases you can enable with this framework:

* Generic question/answering around broad internal company docs
* Knowledge working with specific sub-set of internal knowledge
* Internal comms summary and search
* Research using external providers of information, allowing researchers and writers to explore to information from 3rd parties

This open-source repository contains code that will allow you to get started integrating with some of the most popular datastores. Note that different datastores may have different requirements or limitations that need to be addressed in order to to get good quality responses. While some of the quickstart code has been enhanced to address some of these limitations, others only provide the basics of the integration, and you will need to develop them further to fit your specific use-case and the underlying datastore limitations. 

Please read more about our connectors framework here: LINK TO DOCS

# Getting Started

This project requires Python 3.11+ and [Poetry](https://python-poetry.org/docs/) at a minimum. Each connector uses poetry to create a virtual environment specific to that connector, and to install all the required dependencies to run a local server.

For production releases, you can optionally build and deploy using [Docker](https://www.docker.com/get-started/). When building a Docker image, you can use the `Dockerfile` in the root project directory and specify the `app` build argument.

# Development

For development, refer to a connector's README. Generally, there is an `.env` file that needs to be created in that subdirectory, based off of a `.env-template`. The environment variables here most commonly set authorization values such as API keys, credentials, and also modify the way the search for that connector behaves.

After configuring the `.env`, you will be able to use `poetry`'s CLI to start a local server.

# Integrating With Cohere

All of the connectors in this repository have been tailored to integrate with Cohere's [co.chat](https://docs.cohere.com/reference/chat) API to make creating a grounded chatbot quick and easy.

Cohere's API requires that connectors return documents as an array of JSON objects. Each document should be an object with string keys and string values containing all the relevant information about the document (e.g. `title`, `url`, etc.). For best results the largest text content should be stored in the `text` key.

For example, a connector that returns documents about company expensing policy might return the following:

```json
[
  {
    "title": "Company Travel Policy",
    "text": "Flights, Hotels and Meals can be expensed using this new tool...",
    "url": "https://drive.google.com/file/d/id1"
    "created_at": "2023-11-25T20:09:31Z",
  },
  {
    "title": "2023 Expenses Policy",
    "text": "The list of recommended hotels are",
    "url": "https://drive.google.com/file/d/id2"
    "created_at": "2022-11-22T20:09:31Z",
  }
]
```

Cohere's [co.chat](https://docs.cohere.com/reference/chat) API will query the connector and use these documents to generated answers with direct citations.

# Contributing

Contributions are what drive an open source community, any contributions made are greatly appreciated. For specific. To get started, check out our [documentation.](CONTRIBUTING.md)
