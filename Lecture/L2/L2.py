from flask import Flask, request, jsonify
from pydantic import BaseModel


app = Flask(__name__)


class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True


@app.route('/register', methods=['POST'])
def regiser():
    data = request.get_json()
    try:
        user = User(**data)
        return jsonify({'message': 'success'})
    except BaseException as e:
        return jsonify({'error': str(e)}), 400

    # if "username" not in data or len(data["username"]) < 3:
    #     return jsonify({"error": "Username too short"}), 400
    # if "age" not in data or not isinstance(data["age"], int) or data["age"] < 18:
    #     return jsonify({"error": "Age must be >= 18"}), 400
    # if "email" not in data or "@" not in data["email"]:
    #     return jsonify({"error": "Invalid email"}), 400
    #
    # return jsonify({"message": "User registered successfully"})






if __name__ == '__main__':
    app.run(debug=True)

#

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True

    def __str__(self):
        return self.name


user_1 = User(id=1, name='John', age=20, is_active=True)
print(user_1)


#

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    street: str
    house_number: int


class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True
    address: Address

address = Address(city="New York", street="Green", house_number=1)

user = User(id=1, name="John Doe", age=30, address=address)

print(user)

#

from pydantic import BaseModel, EmailStr, ValidationError


class Address(BaseModel):
    city: str
    street: str
    house_number: int


class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: Address


json_string = """{
    "name": "John Doe",
    "age": 22,
    "email": "john.doe@example.com",
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""


try:
    user = User.model_validate_json(json_string, strict=True)
    print(user)

    print(user.model_dump_json())
except ValidationError as e:
    print(e)

#

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr

    def __str__(self):
        return f"User: {self.username}, Email: {self.email}"


class AdminUser(User):
    access_level: int = 10  # Предоставляем более высокий уровень доступа по умолчанию

    def __str__(self):
        return f"{super().__str__()}, Access Level: {self.access_level}"

    def promote_user(self, user: User):
        print(f"Promoting {user.username} to higher privileges")
        return AdminUser(username=user.username, email=user.email, access_level = self.access_level + 1)


# Создание объекта пользователя
user = User(username='john_doe', email='john.doe@examplecom')
print(user)
# Создание объекта администратора и продвижение пользователя
admin = AdminUser(username='admin_user', email='admin@example.com')
print(admin)
promoted_user = admin.promote_user(user)
print(promoted_user)

#

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    age: int = Field(18, gt=18, description="GT 18")
    is_subscribed: bool = False
    is_active: bool = Field(default=True, description="Can use site")

try:
    user = User(name='Tom', age=10)

    print(user)

    print(user.model_dump_json())

    print(user.model_json_schema())

except Exception as e:
    print(e)

#

from pydantic import BaseModel, field_validator, ValidationError, EmailStr

class User(BaseModel):
    name: str
    age: int
    email: EmailStr

    @field_validator('email')
    def check_email_domain(cls, value: str):
        # allowed_domains = ['example.com', 'test.com']
        # email_domain = value.split('@')[-1]

        email_domain = value.endswith('example.com') or value.endswith('test.com')
        # if email_domain not in allowed_domains:
        if not email_domain:
            raise ValueError(f"Email must be from one of the following domains")
        return value


# Пример создания пользователя
try:
    # Этот email проходит валидацию
    user_valid = User(name="Alice", age=30, email="alice@example.com")
    print(f"Valid user: {user_valid}")
    # Этот email вызовет ошибку валидации
    user_invalid = User(name="Bob", age=25, email="bob@gmail.com")
except ValidationError as e:
    print(e)

#

from pydantic import BaseModel, EmailStr, field_validator, ValidationError


class User(BaseModel):
    name: str
    email: EmailStr

    @field_validator('name')
    def name_validate(cls, value: str):
        if not value.isalpha():
            raise ValueError('Name must be alphanumeric')
        return value

    @field_validator('email')
    def email_validate(cls, value: str):
        if not value.endswith('.com'):
            raise ValueError('Email must end with .com')
        return value


try:
    user_1 = User(name='Tom', email='example@example.com')
except ValidationError as e:
    print(e)

#

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        str_min_length = 2
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M')
        }


user = User(first_name='    ', last_name='Doe', email='tom@example.com', created_at=datetime.now(), updated_at=datetime.now(),)







if __name__ == '__main__':
 app.run(debug=True)