# Box Connector

This package connects Cohere to a Box organization.

## Configuration

To get started, you will require a Box workspace and someone with Administrator rights.

1. Enable 2FA on your Box account, this is required to view an app's client secret.

2. Create a Custom App with Server Authentication (with Client Credentails Grant) in the [Box Developer Console.](https://connectorio.app.box.com/developers/console) The app will require read and write access to all files, because downloading and parsing file contents requires write privileges.

3. From the App's configuration page, note down the Client ID, Client Secret, and Enterprise ID. Use these values for their respective variables in a `.env` file. See `.env-template` for reference.

4. Authorize the App from the [Box Admin Console](https://connectorio.app.box.com/master/custom-apps). Click the top-right `Add App` button and use the same Client ID from step 3.

5. Lastly, you will need to authorize the Service Account Box creates to the folder(s) you'd like to give Cohere read access to. Retrieve the Service Account's email from your app's General Settings tab. Then hover over the folder(s) you'd like to share and invite that email. Best practice would be to create a folder for search purposes, and copy any files you'd like to be searchable in there.

**Note**: Box takes 10+ minutes to index new/copied files, these will not be searchable until then.

### Provision Unstructured

Required: Docker

This connector uses Unstructured to parse the file objects returned by Box. This leverages the Docker image version which hosts their API locally. To get started, head over to [Unstructured](unstructured.io). From here, you can request an API key by signing up. Use this for `BOX_UNSTRUCTURED_API_KEY`.

Next, to use the Docker image, please follow their [documentation.](https://unstructured-io.github.io/unstructured/api.html#using-docker-images)

By default, it spins up the image on localhost:8000, which we are pointing to with `BOX_UNSTRUCTURED_BASE_URL`.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

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
