# SharePoint Quick Start Connector

This package connects Cohere to Microsoft Sharepoint. It features a simple local development setup.

It uses Microsoft Graph API run the search query and return matching files.

# Limitations

The Sharepoint connector currently allows for full-text search based on file contents stored within your Sharepoint instance, it is important to note however that only List items and Drive items are currently returned by the search API.

Important: Sharepoint's default interval for content crawling is set to every 15 minutes. Expect a delay between uploading new files and being able to search for them.

## Configuration

Running this connector requires access to Microsoft 365. For development purposes,
you can register for the Microsoft 365 developer program, which will grant temporary
access to a Microsoft 365.

For the connector to work, you must register the application. To do this, go to the
Microsoft Entra admin center:

https://entra.microsoft.com/

Navigate to Applications > App registrations > New registration option.

Select "Web" as the platform, and ensure you add a redirect URL, even if it is optional.
The redirect URL is required for the admin consent step to work. This connector does not
have a redirect page implemented, but you can use http://localhost/ as the redirect URL.

On the app registration page for the app you have created, go to API permissions, and
grant permissions. For development purposes, you can grant:

- SharePointTenantSettings.Read.All
- SharePointTenantSettings.ReadWrite.All
- Sites.FullControl.All
- Sites.Manage.All
- Sites.Read.All
- Sites.ReadWrite.All
- Sites.Selected

You will then have a create a client secret for the application. Then take the app's credentials (:code:`SHAREPOINT_GRAPH_TENANT_ID`, :code:`SHAREPOINT_GRAPH_CLIENT_ID` and :code:`SHAREPOINT_GRAPH_CLIENT_SECRET`) and copy them into a `.env` file using the `.env-template` as the base template.

To process the files in a readable format by Coral, the Sharepoint connector leverages
In order to process OneDrive files, it is necessary to provide credentials for Unstructured:

- `SHAREPOINT_UNSTRUCTURED_BASE_URL`
- `SHAREPOINT_UNSTRUCTURED_API_KEY`

To use the hosted Unstructured API, you must provide an API key and set `SHAREPOINT_GRAPH_UNSTRUCTURED_BASE_URL`
too. A trailing slash should not be included (i.e. `http://localhost:8000` or `https://api.unstructured.io`).

You can configure which file types will be processed by Unstructured with the `SHAREPOINT_PASSTHROUGH_FILE_TYPES` environment variable. This should be a comma-separated list of strings. Any files matching the types defined will skip Unstructured.

The above environment variables can be read from a .env file. See `.env-template` for an example `.env` file.

After the client has been created, you will need to grant admin consent to the client. One
way to do this is by going to the following URL:

https://login.microsoftonline.com/{site_id}/adminconsent?client_id={client_id}&redirect_uri=http://localhost/

You must replace `{site_id}` and `{client_id}` with the appropriate values. The `redirect_uri`
must match the value that was configured when creating the client in Microsoft Entra.

### Provision Unstructured

Processing the files found on OneDrive requires the Unstructured API. The Unstructured API is
a commercially backed, Open Source project. It is available as a hosted API, Docker image, and as a
Python package, which can be manually set up.

By default, this connector uses the hosted `https://api.unstructured.io` API. You must provide an API key by registering an account and obtaining an API key [here](https://unstructured.io/api-key).

Alternatively, you can use the API by hosting it yourself with their provided Docker image. If you've used Docker before, the setup is relatively straightforward. Please follow the instructions for setting up the Docker image in the Unstructured [documentation](https://unstructured-io.github.io/unstructured/api.html#using-docker-images).

The final option is to set Unstructured up locally, outside of Docker. This is a complex option that is not recommended, as it involves installing many dependencies outside of Python.

### Run Flask Server

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

To run the Flask server in development mode, please run:

```bash
  poetry run flask --app provider --debug run
```

The Flask API will be bound to :code:`localhost:5000`.

```bash
  curl --request POST \
    --url http://localhost:3000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "Weber charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
