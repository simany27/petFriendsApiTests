from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name="Рада", animal_type="Хорек", age="4", pet_photo="images/horek.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name

def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/horek.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_pet_info(name='Мурзило', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        raise Exception("There is no my pets")
    else:
        pet_id = my_pets["pets"][0]["id"]

        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result["name"] == name

def test_1_successful_create_pet_simple(name="Госпожа", animal_type="Выдра", age="1"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_2_unsuccessful_create_pet_simple(name='Марианна', animal_type='Выдра', age='1'):
    incorrect_auth_key = {'key': '12345'}
    status, result = pf.create_pet_simple(incorrect_auth_key, name, animal_type, age)
    assert status == 403

def test_3_successful_add_photo_of_pet(pet_photo="images/vidra.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        raise Exception("There is no my pets")
    else:
        pet_id = my_pets["pets"][0]["id"]
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result["pet_photo"]

def test_4_unsuccessful_add_photo_of_pet(pet_photo="images/vidra.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        raise Exception("There is no my pets")
    else:
        pet_id = my_pets["pets"][0]["id"]
        incorrect_auth_key = {'key': '12345'}
        status, result = pf.add_photo_of_pet(incorrect_auth_key, pet_id, pet_photo)
        assert status == 403

def test_5_unsuccessful_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/horek.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]["id"]
    incorrect_auth_key = {'key': '12345'}
    status, _ = pf.delete_pet(incorrect_auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 403

def test_6_unsuccessful_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/horek.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    first_pet_name = my_pets['pets'][0]['name']
    incorrect_pet_id = '12345'
    status, _ = pf.delete_pet(auth_key, incorrect_pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   # т.к. при неуспехе, код все равно 200, проверяем что не удалилось так:
    assert first_pet_name == my_pets['pets'][0]['name']

def test_7_get_api_key_for_invalid_email(email='fjf@kkk.ru', password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_8_get_api_key_for_invalid_password(email=valid_email, password='chachacha'):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_9_unsuccessful_update_pet_info(name='Мармелад', animal_type='Кот', age=-4):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        raise Exception("There is no my pets")
    else:
        incorrect_pet_id = '12345'
        status, result = pf.update_pet_info(auth_key, incorrect_pet_id, name, animal_type, age)
        assert status == 400

def test_10_unsuccessful_update_pet_info(name='Мармелад', animal_type='Кот', age=-4):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        raise Exception("There is no my pets")
    else:
        pet_id = my_pets["pets"][0]["id"]
        incorrect_auth_key = {'key': '12345'}
        status, result = pf.update_pet_info(incorrect_auth_key, pet_id, name, animal_type, age)
        assert status == 403