#!/bin/bash

# start Vespa
bash /usr/local/bin/start-container.sh &

# wait until Vespa config server is ready
until curl -s http://localhost:19071/state/v1/health; do sleep 5; done

# deploy application
/opt/vespa/bin/vespa-deploy prepare /opt/vespa/conf/vespa
/opt/vespa/bin/vespa-deploy activate

# keep container running
tail -f /dev/null
