import pytest

# export PYTHONPATH = "~/develop/work4/"
from tests.test_openbrewerydb_org.test_data.test_data import ids, cities


def test_get_list_breweries(base_url, http_method_get):
    target = base_url + "breweries"
    response = http_method_get(url=target)
    list_all_breweries = response.json()

    assert response.status_code == 200
    assert len(list_all_breweries) == 20


def test_compare_response_data_in_breweries_list(base_url, http_method_get,
                                                 get_expected_json_breweries_list):
    target = base_url + "breweries"
    response = http_method_get(url=target)
    actual_json_breweries_list = response.json()

    assert get_expected_json_breweries_list == actual_json_breweries_list


@pytest.mark.parametrize("city", cities)
def test_get_list_breweries_filtered_by_city_sep_by_(base_url, http_method_get, city):
    target = base_url + f"breweries?by_city={city.replace(' ', '_')}"
    response = http_method_get(url=target)

    assert response.status_code == 200
    assert response.json()
    assert response.json()[0]['city'] == city


@pytest.mark.parametrize("city", ["San Diego", "Castle Rock", "John Day", "Killeshin", "Gilbert"])
def test_get_list_breweries_filtered_by_city_sep_by_percent(base_url, http_method_get, city):
    target = base_url + f"breweries?by_city={city.replace(' ', '%20')}"
    response = http_method_get(url=target)

    assert response.status_code == 200
    assert response.json()
    assert response.json()[0]['city'] == city


@pytest.mark.parametrize("city", ["City One", "CityTwo", "City_Three", "City%20Four"])
def test_get_list_breweries_filtered_by_city_negative(base_url, http_method_get, city):
    target = base_url + f"breweries?by_city={city.replace(' ', '_')}"
    response = http_method_get(url=target)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("name", ["cooper", "modern times", "dog", "cat", "north", "west",
                                  "12 gates"])
def test_get_list_breweries_filtered_by_name(base_url, http_method_get, name):
    target = base_url + f"breweries?by_name={name.replace(' ', '_')}"
    response = http_method_get(url=target)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json

    for element in response_json:
        assert element["name"].lower().find(name) >= 0


@pytest.mark.parametrize("type_", ["micro", "nano", "regional", "brewpub", "large", "planning",
                                   "bar", "contract", "closed"])
def test_get_list_breweries_filtered_by_type(base_url, http_method_get, type_):
    target = base_url + f"breweries?by_type={type_}"
    response = http_method_get(url=target)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json

    for element in response_json:
        assert element["brewery_type"].lower() == type_


@pytest.mark.parametrize("type_", ["micro_", "_nano", "regional_", "brew_pub", "large_new",
                                   "proprietor", "close"])
def test_get_list_breweries_filtered_by_type_negative(base_url, http_method_get, type_):
    target = base_url + f"breweries?by_type={type_}"
    response = http_method_get(url=target)
    response_json = response.json()

    assert response.status_code == 400
    assert response_json["errors"][0] == 'Brewery type must include one of these types: ["micro",' \
                                         ' "nano", "regional", "brewpub", "large", "planning", ' \
                                         '"bar", "contract", "proprieter", "closed"]'
