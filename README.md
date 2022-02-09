# work4
Тестирование API

Before run tests:

1. Export env variable:
export PYTHONPATH="~/develop/work4/"

2. Run tests
pytest -vs tests/
pytest -vs tests/test_check_response_status_code
pytest -vs tests/test_dog_ceo
pytest -vs tests/test_dog_ceo/test_dog_ceo.py
pytest -vs tests/test_dog_ceo/test_dog_ceo.py::test_get_multiple_random_images     

Or run tests like this:
PYTHONPATH="~/develop/work4/ 
pytest -vs tests/


