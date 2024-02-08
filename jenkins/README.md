# Jenkins Connector

This project connects Cohere with Jenkins.

## Configuration

The search connector requires the following environment variables:

```
JENKINS_SERVER_URL

This variable should contain the URL to the Jenkins server.
```

```
JENKINS_USER_NAME

This variable should contain the username for the Jenkins server.
```

```
JENKINS_API_KEY

This variable should contain the API key for the Jenkins server.
```

```
JENKINS_CONNECTOR_API_KEY

This variable should contain the API key for the Jenkins connector.
```

### Optional configuration

```
JENKINS_FOLDER_DEPTH

Number of levels to search. By default 0, which will limit search to toplevel.
```

```
JENKINS_FOLDER_DEPTH_PER_REQUEST

Number of levels to fetch at once. By default 10, which is usually enough to fetch all jobs using a single request and still easily fits into an HTTP request.
```

## Development

To set up Jenkins locally use next docker command from dev folder:

```bash
docker network create jenkins
docker build -t myjenkins-blueocean:2.414.2-1 .
docker run --name jenkins-blueocean --restart=on-failure --detach \
  --network jenkins --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 --publish 50000:50000 \
  --volume <your path>/jenkins-data:/var/jenkins_home \
  --volume <your path>/jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:2.414.2-1


```

Create a virual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything is working

```bash
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
