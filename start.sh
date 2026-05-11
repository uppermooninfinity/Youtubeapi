# start.sh

uvicorn main:app \
--host 0.0.0.0 \
--port 9090 \
--workers 4 \
--loop uvloop \
--http httptools
