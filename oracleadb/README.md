
# ADBS-QuickStart-Connector


## What is this connector?

https://github.com/cohere-ai/quick-start-connectors


This project allows you to create a simple connection and query Oracle ADBS that can be used with Cohere's Chat API for RAG.

## Limitations

The ADBS connector only allows search within a specific table, and for specific text columns only.

## Connecting Plugin to Oracle ADB Instance (Hosted Anywhere)

### TLS (Wallet Less)
 
With TLS enabled in your Oracle ADB Deployment, plugin can connect to Oracle ADB without using a wallet. Both Thin and Thick modes of the python-oracledb driver support TLS. For TLS you need username, password and dsn.

Follow this ```  .env_template ``` for TLS

```
##Connection Env Vars##
ORACLEADB_USER=my_adb_username
ORACLEADB_PASSWORD=my_adb_password
ORACLEADB_DSN=(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.example.oraclecloud.com))(connect_data=(service_name=example_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))
ORACLEADB_CONNECTION_TYPE=TLS

##Plugin Specific Env Vars##
ORACLEADB_TABLE_NAME=employee
ORACLEADB_FTS_COLUMN=employee_reviews, technical_feedback
ORACLEADB_AUTO_INDEX_FTS_COLUMNS=True
ORACLEADB_CONNECTOR_API_KEY=
```

Refer to Oracle documentation to connect to an ADB instance using TLS authentication and the blog post Easy wallet-less connections to Oracle Autonomous Databases in Python to enable TLS for your Oracle ADB instance.

### mTLS (wallet based, for enanched security)
This plugin only needs Thin Mode connectivity so in Thin mode, only two files from the zip are needed:

-   `tnsnames.ora`  - Maps net service names used for application connection strings to your database services
    
-   `ewallet.pem`  - Enables SSL/TLS connections in Thin mode. Keep this file secure

Follow this `.env_template` for mTLS

```
##Connection Env Vars##
ORACLEADB_USER=my_adb_username 
ORACLEADB_PASSWORD=my_adb_password 
ORACLEADB_DSN=(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.example.oraclecloud.com))(connect_data=(service_name=example_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))
ORACLEADB_CONNECTION_TYPE=mTLS
ORACLEADB_WALLET_LOCATION=downloaded_wallet_location 
ORACLEADB_WALLET_PASSWORD=downloaded_wallet_password

##Plugin Specific Env Vars##
ORACLEADB_TABLE_NAME=employee
ORACLEADB_FTS_COLUMN=employee_reviews, technical_feedback ORACLEADB_AUTO_INDEX_FTS_COLUMNS=True
ORACLEADB_CONNECTOR_API_KEY=
``` 
  

## Development

Create a ``` .env ``` file with the following fields (refer .env-template)

```
##Connection Env Vars##
ORACLEADB_USER=admin 
ORACLEADB_PASSWORD=Adm_password1 
ORACLEADB_DSN=(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.example.oraclecloud.com))(connect_data=(service_name=example_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))
ORACLEADB_CONNECTION_TYPE=mTLS
ORACLEADB_WALLET_LOCATION=downloaded_wallet_location 
ORACLEADB_WALLET_PASSWORD=downloaded_wallet_password

##Plugin Specific Env Vars##
ORACLEADB_TABLE_NAME=employee
ORACLEADB_FTS_COLUMN=employee_reviews, technical_feedback ORACLEADB_AUTO_INDEX_FTS_COLUMNS=True
ORACLEADB_CONNECTOR_API_KEY=

##For Local Docker Development##
WALLET_PASSWORD=Wall_password1
ADMIN_PASSWORD=Adm_password1
WORKLOAD_TYPE=ADW
```

Currently the code automatically indexes the columns given in the ``` .env ``` file below as per below, if ``` ORACLE_AUTO_INDEX_FTS_COLUMNS ``` is set to ``` True ```

```
begin
ctx_ddl.create_preference('STEM_FUZZY_PREF', 'BASIC_WORDLIST');
ctx_ddl.set_attribute('STEM_FUZZY_PREF','FUZZY_MATCH','ENGLISH');
ctx_ddl.set_attribute('STEM_FUZZY_PREF','FUZZY_SCORE','1');
ctx_ddl.set_attribute('STEM_FUZZY_PREF','FUZZY_NUMRESULTS','5000');
ctx_ddl.set_attribute('STEM_FUZZY_PREF','SUBSTRING_INDEX','TRUE');
ctx_ddl.set_attribute('STEM_FUZZY_PREF','STEMMER','ENGLISH');
end;
/
```
Start ADBS server with

```
$ docker-compose up
```
After the container is healthy, (note that ORACLE_CONFIG_DIR and ORACLE_WALLET_DIR should point to this location in the .env file)

```
$ docker cp adb-free:/u01/app/oracle/wallets/tls_wallet /scratch/tls_wallet
```

To start your local Flask server, create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```
$ python3.11 -m venv .venv

$ source .venv/bin/activate

$ pip3 install poetry

$ poetry install
```

After this step you can run the following test to see that Python-DB is working as expected (2 tests must pass)

```
$ python3.11 -m pytest --disable-warnings
```

Then you can start the server and curl the endpoints like below

```

$ poetry run flask --app provider --debug run --port 5000

```

```
$ curl --request POST \
--url http://localhost:5000/search \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
--data '{
"query": "What could be the most favorite food of honest and hardworking employees?"
}'
```

Alternatively, load up the Swagger UI and try out the API from a browser: [http://localhost:5000/ui/](http://localhost:5000/ui/)