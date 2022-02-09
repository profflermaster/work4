import pytest

# export PYTHONPATH = "~/develop/work4/"
from tests.test_dog_ceo.test_data.test_data import breeds


@pytest.fixture
def base_url():
    return "https://dog.ceo/"


@pytest.fixture
def get_dict_all_breeds(base_url, http_method_get):
    target = base_url + "api/breeds/list/all"
    response = http_method_get(url=target)
    dict_all_breeds = response.json()
    return dict_all_breeds


# Пример использования параметризации фикстуры ('breeds' - генератор)
@pytest.fixture(params=breeds, scope='session')
def get_breed_from_list(request):
    return request.param
