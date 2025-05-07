import allure
import pytest
import requests
from pydantic import ValidationError

from core.models.booking import BookingResponse


@allure.feature('Test creatig booking')
@allure.story('Pozitive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname" : "Jimmy",
        "lastname" : "Browning",
        "totalprice" : 150,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-01-01",
            "checkout" : "2018-01-10"
        },
        "additionalneeds" : "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname'], "Имя не совпадает"
    assert response['booking']['lastname'] == booking_data['lastname'], "Фамилия не совпадает"
    assert response['booking']['totalprice'] == booking_data['totalprice'], "Цена не совпадает"
    assert response['booking']['depositpaid'] == booking_data['depositpaid'], "Депозит не совпадает"
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "Дата заезда не совпадает"
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "Дата выезда не совпадает"
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds'], "Дополнительные нужды не совпадают"


@allure.feature('Test creatig booking')
@allure.story('Pozitive: creating booking with random data')
def test_create_booking_with_random_data(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname'], "Имя не совпадает"
    assert response['booking']['lastname'] == booking_data['lastname'], "Фамилия не совпадает"
    assert response['booking']['totalprice'] == booking_data['totalprice'], "Цена не совпадает"
    assert response['booking']['depositpaid'] == booking_data['depositpaid'], "Депозит не совпадает"
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "Дата заезда не совпадает"
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "Дата выезда не совпадает"
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds'], "Дополнительные нужды не совпадают"

@allure.feature('Test creatig booking')
@allure.story('Pozitive: creating booking without additional needs')
def test_create_booking_without_additional_needs(api_client):
    booking_data = {
        "firstname": "Bob",
        "lastname": "Browning",
        "totalprice": 350,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2018-01-10"
        }
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert 'additionalneeds' not in response['booking'], "Параметр additionalneeds не должен присутствовать"


@allure.feature('Test creatig booking')
@allure.story('Pozitive: creating booking with minimal values')
def test_create_booking_with_minimal_values(api_client):
    booking_data = {
        "firstname": "A",
        "lastname": "B",
        "totalprice": 0,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-11"
        },
        "additionalneeds": ""
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']


@allure.feature('Test creatig booking')
@allure.story('Negative: creating booking with checkin = checkout')
def test_create_booking_with_checkin_checkout(api_client):
    booking_data = {
        "firstname": "Alex",
        "lastname": "Brown",
        "totalprice": 1000,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2023-01-11",
            "checkout": "2023-01-11"
        },
        "additionalneeds": ""
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']


@allure.feature('Test creatig booking')
@allure.story('Pozitive: create booking returns unique id')
def test_create_booking_returns_unique_id(api_client, generate_random_booking_data):
    booking_data1 = generate_random_booking_data
    response_data1 = api_client.create_booking(booking_data1)
    booking_data2 = generate_random_booking_data
    response_data2 = api_client.create_booking(booking_data2)

    assert response_data1['bookingid'] != response_data2['bookingid'], "ID брони должны быть уникальны"



@allure.feature('Test creating booking')
@allure.story('Negative: missing required field - firstname')
def test_create_booking_missing_firstname(api_client):
    booking_data = {
        # "firstname": "John",  # Отсутствует
        "lastname": "Dumany",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-10"
        }
    }

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        api_client.create_booking(booking_data)

    assert excinfo.value.response.status_code == 500, "Ожидался статус-код 500"
    assert "Invalid JSON" in excinfo.value.response.text or "Internal Server Error"













