import allure
import pytest
import requests


@allure.feature('Test Ping')
@allure.story('Test connection')
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f'Expected status 201 but got {status_code}'


@allure.feature('Test Ping')
@allure.story('Test server unavailability')
def test_ping_server_unavailable(api_client, mocker):
    # Мокируем метод `get` с ошибкой "Server unavailable"
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailable"))

    # Проверяем, что вызов `api_client.ping()` генерирует исключение с ожидаемым текстом
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test wrong HTTP method')
def test_ping_wrong_http_method(api_client, mocker):
    # Создаем мок-объект для ответа сервера
    mock_response = mocker.Mock()
    mock_response.status_code = 405  # Устанавливаем статус-код 405 (Method Not Allowed)

    # Мокируем метод `get` с возвратом созданного мок-ответа
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)

    # Проверяем, что вызов `api_client.ping()` генерирует исключение с ожидаемым текстом
    with pytest.raises(AssertionError, match="Expected status 201 but got 405"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    # Создаем мок-объект для ответа сервера
    mock_response = mocker.Mock()
    mock_response.status_code = 500  # Устанавливаем статус-код 500 (Internal Server Error)

    # Мокируем метод `get` с возвратом созданного мок-ответа
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)

    # Проверяем, что вызов `api_client.ping()` генерирует исключение с ожидаемым текстом
    with pytest.raises(AssertionError, match="Expected status 201 but got 500"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test wrong URL')
def test_ping_not_found(api_client, mocker):
    # Создаем мок-объект для ответа сервера
    mock_response = mocker.Mock()
    mock_response.status_code = 404  # Устанавливаем статус-код 404

    # Мокируем метод `get` с возвратом созданного мок-ответа
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)

    # Проверяем, что вызов `api_client.ping()` генерирует исключение с ожидаемым текстом
    with pytest.raises(AssertionError, match="Expected status 201 but got 404"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test connection with different success code')
def test_ping_not_found(api_client, mocker):
    # Создаем мок-объект для ответа сервера
    mock_response = mocker.Mock()
    mock_response.status_code = 200

    # Мокируем метод `get` с возвратом созданного мок-ответа
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)

    # Проверяем, что вызов `api_client.ping()` генерирует исключение с ожидаемым текстом
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    # Мокируем метод `get` с ошибкой Timeout
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)

    # Проверяем, что вызов `api_client.ping()` генерирует исключение `requests.Timeout`
    with pytest.raises(requests.Timeout):
        api_client.ping()




