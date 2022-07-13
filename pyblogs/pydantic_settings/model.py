from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional, Sequence

from pyblogs.pydantic_settings.settings_schema import AppSettings


class MLModel(metaclass=ABCMeta):

    @abstractmethod
    def predict(self, vector: Sequence[float]) -> float:
        ...


class MockedModel(MLModel):

    def __init__(self, ret_value: float) -> None:
        super().__init__()
        self.ret_value = ret_value

    def predict(self, vector: Sequence[float]) -> float:
        print('Mocked model prediction')
        return self.ret_value


class RestModel(MLModel):

    def __init__(self, url: str, timeout: Optional[int]) -> None:
        super().__init__()
        self.url = url
        self.timeout = timeout

    def predict(self, vector: Sequence[float]) -> float:
        print(f'rest model -- {self.url}')
        # TODO real implementation of calling the rest API
        return vector[0]


def simple_factory(app_settings: AppSettings) -> MLModel:
    # the simplest if-else factory, not the scope of blog
    settings = app_settings.ml_model
    if settings.model_type == 'mocked':
        return MockedModel(settings.ret_val)
    elif settings.model_type == 'rest':
        return RestModel(settings.http_endpoint, settings.timeout)
    else:
        raise NotImplementedError(f'unable to instantiate model {settings}')


def dict_factory(app_settings: Dict[str, Any]) -> MLModel:
    settings = app_settings['ml_model']
    if settings['model_type'] == 'mocked':
        # do some validation
        return MockedModel(settings['ret_val'])
    elif settings['model_type'] == 'rest':
        # do some validation
        return RestModel(settings['http_endpoint'], settings.get('timeout'))
    else:
        raise NotImplementedError(f'unable to instantiate model {settings}')
