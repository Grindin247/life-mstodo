#TODO: Add a fancy banner

import argparse
import pathlib

from fastapi import FastAPI
from api.src.openapi_server.mstodo import MsTodoLifeService
import uvicorn

from openapi_server.apis.list_api import router as ListApiRouter

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, type=pathlib.Path, help="Path to the configuration file")
    args = parser.parse_args()

    mstodo = MsTodoLifeService(args.config)

    mstodo.startPolling()

    app = FastAPI(
    title="LIFE MS Todo API",
    description="This interface provides access to personal MS TODO list.",
    version="0.0.1",
    )

    app.include_router(ListApiRouter)

    uvicorn.run(app)
