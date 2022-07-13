from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, validator


class MockedModelSettings(BaseSettings):
    model_type: Literal['mocked']
    ret_val: float

    @validator('ret_val')
    def must_be_0_to_1(cls, v):
        if 0 <= v <= 1:
            return v
        raise ValueError(f'ret_val must be in 0 - 1 range, given {v}')


class RestModelSettings(BaseSettings):
    model_type: Literal['rest']
    http_endpoint: AnyHttpUrl
    timeout: Optional[int] = None

    @validator('timeout')
    def timeout_must_not_be_negative(cls, v):
        if v and v < 0:
            raise ValueError(f'timeout must not be negative, given {v}')
        return v


class AppSettings(BaseSettings):
    ml_model: Union[
        MockedModelSettings,
        RestModelSettings
    ] = Field(..., discriminator='model_type')
    # some other settings
