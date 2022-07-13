
# Poor man's tests

from pydantic import ValidationError

from pyblogs.pydantic_settings.model import dict_factory, simple_factory
from pyblogs.pydantic_settings.settings_schema import AppSettings

MOCKED_EXAMPLE_OK = {
    'ml_model': {
        'model_type': 'mocked',
        'ret_val': 0.6
    }
}

MOCKED_EXAMPLE_FAULT = {
    'ml_model': {
        'model_type': 'mocked',
        'ret_val': -0.1
    }
}

REST_EXAMPLE_OK = {
    'ml_model': {
        'model_type': 'rest',
        'http_endpoint': 'http://localhost:9050/model',
        'timeout': 10
    }
}

REST_EXAMPLE_FAULT = {
    'ml_model': {
        'model_type': 'rest',
        'http_endpoint': 'invalid_url',
        'timeout': '20'
    }
}


def dict_examples() -> None:
    mocked_ok = dict_factory(MOCKED_EXAMPLE_OK)
    print(mocked_ok.predict([10, 20, 30]))
    mocked_fault = dict_factory(MOCKED_EXAMPLE_FAULT)
    print(mocked_fault.predict([10, 20, 30]))
    rest_ok = dict_factory(REST_EXAMPLE_OK)
    print(rest_ok.predict([10, 20, 30]))
    rest_fault = dict_factory(REST_EXAMPLE_FAULT)
    print(rest_fault.predict([10, 20, 30]))


def pydantic_examples() -> None:
    mocked_ok = simple_factory(AppSettings.parse_obj(MOCKED_EXAMPLE_OK))
    print(mocked_ok.predict([1, 2, 3]))

    try:
        mocked_fault = simple_factory(
            AppSettings.parse_obj(MOCKED_EXAMPLE_FAULT))
    except ValidationError as ex:
        print(f'{ex}')

    rest_ok = simple_factory(AppSettings.parse_obj(REST_EXAMPLE_OK))
    print(rest_ok.predict([1, 2, 3]))

    try:
        rest_fault = simple_factory(
            AppSettings.parse_obj(REST_EXAMPLE_FAULT))
    except ValidationError as ex:
        print(f'{ex}')


def main() -> None:
    print("PYDANTIC EXAMPLES")
    pydantic_examples()
    print('DICT EXAMPLES')
    dict_examples()


if __name__ == '__main__':
    main()
