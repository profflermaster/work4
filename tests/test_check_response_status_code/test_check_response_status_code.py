import pytest


def test_url_status(base_url, status_code, request_method):
    """Тестовая функция для проверки работы параметров, переданных в виде аргументов 'pytest'
    Пример запуска: pytest test_check_response_status_code.py::test_url_status
    --url=https://mail.ru --status_code=200"""

    target = base_url
    response = request_method(url=target)

    assert str(response.status_code) == status_code


@pytest.mark.parametrize("status_code", [200, 300, 400, 404, 500, 502])
def test_url_status_test(request_method, status_code):
    """Тест для проверки корректности работы проверки кодов ответа без 'pytest.addoption.' с
     использованием тестового ресурса https://httpbin.org."""

    target = f"https://httpbin.org/status/{status_code}"
    response = request_method(url=target)

    assert response.status_code == status_code