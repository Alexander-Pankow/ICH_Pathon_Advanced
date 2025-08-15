"""
Разработать систему регистрации пользователя,
используя Pydantic для валидации входных данных,
обработки вложенных структур и сериализации.
Система должна обрабатывать данные в формате JSON.
Задачи:
Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
валидирует данные,
и в случае успеха сериализует объект обратно в JSON и возвращает его.
Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
Написать несколько примеров JSON строк для проверки различных сценариев валидации:
успешные регистрации и случаи,
когда валидация не проходит (например возраст не соответствует статусу занятости).

Модели:
Address: Должен содержать следующие поля:
city: строка, минимум 2 символа.
street: строка, минимум 3 символа.
house_number: число, должно быть положительным.
User: Должен содержать следующие поля:
name: строка, должна быть только из букв, минимум 2 символа.
age: число, должно быть между 0 и 120.
email: строка, должна соответствовать формату email.
is_employed: булево значение, статус занятости пользователя.
address: вложенная модель адреса.
Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true),
его возраст должен быть от 18 до 65 лет.


# Пример JSON данных для регистрации пользователя

json_input = {
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""

from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator, ValidationInfo
import json

class Address(BaseModel):
    city: str = Field(..., min_length=2, description="City name must have at least 2 characters")
    street: str = Field(..., min_length=3, description="Street name must have at least 3 characters")
    house_number: int = Field(..., gt=0, description="House number must be positive")


class User(BaseModel):
    name: str = Field(..., pattern=r"^[A-Za-z\s]{2,50}$", description="Name must contain only letters and spaces")
    is_employed: bool = Field(default=True, description="Is employed must be true")
    age: int = Field(..., ge=0, le=120, description="Age must be between 0 and 120")
    email: EmailStr = Field(..., description="Email address must have at least 2 characters")
    address: 'Address' = Field(..., description="Address must have at least 2 characters")

    @field_validator("age")
    def check_employment_age(cls, value, info: ValidationInfo):
        """
               EN: If user is employed, age must be between 18 and 65.
               RU: Если пользователь работает, возраст должен быть от 18 до 65.
        """
        is_employed = info.data.get("is_employed")
        if is_employed and not (18 <= value <= 65):
            raise ValueError("If employed, age must be between 18 and 65")
        return value

# Вот так, как вы советовали: "не валидные" варианты выдает ошибки нормально,
# но "валидные" не выдаёт,
# говорит что "Вы используете parse_raw — это старый метод Pydantic v1."

def process_user_registration(json_data: str) -> str:
    """
        EN: Receives JSON string, validates with Pydantic, returns serialized JSON or error.
        RU: Принимает JSON-строку, валидирует через Pydantic, возвращает сериализованный JSON или ошибку.
    """
    try:
        user = User.parse_raw(json_data)
        return user.json()
    except ValidationError as e:
        return str(e)

#Вот  этот вариант написал GPT и принт хороший.

# def process_user_registration(json_data: str) -> str:
#     """
#     RU: Принимает JSON-строку, валидирует через Pydantic, возвращает сериализованный JSON или ошибку.
#     """
#     try:
#         user = User.model_validate_json(json_data, strict=True)
#         return user.model_dump_json(indent=4)
#     except ValidationError as e:
#         # Возвращаем уже готовый JSON с ошибками, без ссылок на pydantic.dev
#         errors = []
#         for err in e.errors():
#             errors.append({
#                 "field": ".".join(str(loc) for loc in err["loc"]),
#                 "message": err["msg"]
#             })
#         return json.dumps({"error": errors}, indent=4)

# Test JSONs

if __name__ == "__main__":
    # Valid example
    valid_json = """{
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""

    # Invalid: employed but too old
    invalid_age_json = """{
        "name": "John Doe",
        "age": 70,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""

    # Invalid: short city name
    invalid_city_json = """{
        "name": "Jane Smith",
        "age": 25,
        "email": "jane.smith@example.com",
        "is_employed": false,
        "address": {
            "city": "A",
            "street": "Main Street",
            "house_number": 45
        }
    }"""

print("=== Valid registration ===")
print(process_user_registration(valid_json))
print("\n=== Invalid (employment age) ===")
print(process_user_registration(invalid_age_json))
print("\n=== Invalid (city length) ===")
print(process_user_registration(invalid_city_json))