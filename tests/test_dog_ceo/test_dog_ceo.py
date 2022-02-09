import json
import collections
import pytest
import os

# export PYTHONPATH="/~/develop/work4/"
from tests.test_dog_ceo.test_data.test_data import breeds
from pathlib import Path

CUR_DIR = Path(__file__).parent
TEST_DIR_PATH = f'{CUR_DIR}/download_images'

# Check whether the specified TEST_DIR_PATH exists or not
isExist = os.path.exists(TEST_DIR_PATH)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(TEST_DIR_PATH)


@pytest.mark.parametrize("image_count", [1, 3, 10, 25, 50])
def test_get_multiple_random_images(base_url, image_count, http_method_get):
    target = base_url + f"api/breeds/image/random/{image_count}"
    response = http_method_get(url=target)
    assert len(response.json()['message']) == image_count


@pytest.mark.parametrize("image_count", [-1, 0, 51])
def test_get_multiple_random_images_negative(base_url, image_count, http_method_get):
    target = base_url + f"api/breeds/image/random/{image_count}"
    response = http_method_get(url=target)

    with pytest.raises(AssertionError):
        assert len(response.json()['message']) == image_count


def test_check_all_main_breeds_count(base_url, http_method_get, get_dict_all_breeds):
    target = base_url + "api/breeds/list/all"
    response = http_method_get(url=target)

    assert response.status_code == 200
    assert get_dict_all_breeds['status'] == "success"
    assert len(get_dict_all_breeds['message']) == 95


def test_check_all_items_in_dict_all_breeds(get_dict_all_breeds):
    with open(f"{CUR_DIR}/test_data/list_all_breeds.json", "r") as json_file:
        dict_all_breeds_expected = json.loads(json_file.read())

    # Сравниваем 2 словаря (элементы в словарях могут располагаться в разной последовательности)
    assert get_dict_all_breeds['message'] == dict_all_breeds_expected


def test_get_breed_image_from_breed_list(base_url, http_method_get, get_breed_from_list):
    target = base_url + f"api/breed/{get_breed_from_list}/images/random"
    response = http_method_get(url=target)
    image_url = response.json()['message']
    response_image = http_method_get(url=image_url, stream=True)

    with open(f"{TEST_DIR_PATH}/image_"
              f"{''.join(c if c != '/' else '_' for c in get_breed_from_list)}.jpg", "wb") as f:
        for chunk in response_image.iter_content(chunk_size=128):
            f.write(chunk)

    assert response.status_code == 200
    assert response_image.status_code == 200


def test_display_single_random_image(base_url, http_method_get):
    target = base_url + "api/breeds/image/random"
    response = http_method_get(url=target)
    random_image_url = response.json()['message']
    response_random_image = http_method_get(url=random_image_url)

    assert response.status_code == 200
    assert response_random_image.status_code == 200
    assert response.json()['status'] == "success"
