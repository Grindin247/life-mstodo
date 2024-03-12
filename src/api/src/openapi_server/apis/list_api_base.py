# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401



class BaseListApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseListApi.subclasses = BaseListApi.subclasses + (cls,)
    def list_name_get(
        self,
        name: str,
    ) -> List[str]:
        """Get todo list by name"""
        ...
