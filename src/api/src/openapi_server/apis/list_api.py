# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.list_api_base import BaseListApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/list/{name}",
    responses={
        200: {"model": List[str], "description": "OK"},
    },
    tags=["List"],
    summary="Get todo list",
    response_model_by_alias=True,
)
async def list_name_get(
    name: str = Path(..., description="Name of the list"),
) -> List[str]:
    """Get todo list by name"""
    return BaseListApi.subclasses[0]().list_name_get(name)
