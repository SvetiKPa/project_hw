# city: строка, минимум 2 символа.
# street: строка, минимум 3 символа.
# house_number: число, должно быть положительным.
# User: Должен содержать следующие поля:
# name: строка, должна быть только из букв, минимум 2 символа.
# age: число, должно быть между 0 и 120.
# email: строка, должна соответствовать формату email.
# is_employed: булево значение, статус занятости пользователя.
# address: вложенная модель адреса.

from pydantic import BaseModel, EmailStr, ValidationError, Field, ConfigDict, field_validator


class Address(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True            # Валидация работает даже при изменении полей после создания
    )
    city: str = Field(..., min_length=2)    # 2
    street: str = Field(..., min_length=3)  # 3
    house_number: int = Field(gt=0)         # >0


class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )
    name: str = Field(..., min_length=2)  # min 2
    age: int = Field(..., gt=0, le=120)  # 0-120
    email: EmailStr
    is_employed: bool = Field(description='если (is_employed = true), его возраст должен быть от 18 до 65 лет.')
    address: Address

    @field_validator('is_employed', mode="after")
    @classmethod
    def check_age_employment(cls, is_employed: bool, info) -> bool:
#        print(info.data)
        age = info.data.get('age')
        # if is_employed is None:
        #     return age
        if is_employed and age is not None and (age < 18 or age > 65):
            raise ValueError('Работающий пользователь должен быть в возрасте от 18 до 65 лет')
        return is_employed


json_data = ["""{   "name": "John Doe     ",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }  }""",
     """{   "name": " Jo",
         "age": 18,
         "email": "john.doe@example.com",
         "is_employed": true,
         "address": {
             "city": "New ",
             "street": "5th Avenue",
             "house_number": 1
         }}""",
     """{   "name": " Joli",
          "age": 25,
          "email": "joli.doe@example.com",
          "is_employed": true,
          "address": {
              "city": "New ",
              "street": "5th Avenue",
              "house_number": 25
          }}"""

             ]

for data in json_data:
    try:
        user = User.model_validate_json(data)
        print(f"{user.name}, {user.email}, {user.age}, {user.is_employed}")
        print(user.model_dump_json(indent=4))
    except ValidationError as e:
        print(e)
