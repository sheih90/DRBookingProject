import allure
import pytest
import requests

@allure.feature('Test Booking')
@allure.story('Test create booking')
def test_create_booking(api_client, generate_random_booking_data):

    with allure.step('Создание новой брони'):
        booking_data = generate_random_booking_data
        response_data = api_client.create_booking(booking_data)

    with allure.step('Проверка данных ответа'):
        assert 'bookingid' in response_data, "Ответ должен содержать 'bookingid'"
        assert isinstance(response_data['bookingid'], int), "'bookingid' должен быть числом"
        booking_response = response_data['booking']
        assert booking_response['firstname'] == booking_data['firstname'], "Имя не совпадает"
        assert booking_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает"
        assert booking_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает"
        assert booking_response['depositpaid'] == booking_data['depositpaid'], "Депозит не совпадает"
        assert booking_response['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_response['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда не совпадает"