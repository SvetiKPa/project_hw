from pydantic import BaseModel, EmailStr, ValidationError, Field, ConfigDict, field_validator


class Address(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True  # Валидация работает даже при изменении полей после создания
    )
    city: str = Field(min_length=2)   #2
    street: str = Field(min_length=3) #3
    house_number: int = Field(gt=0)   #>0


class User(BaseModel):
    model_config = ConfigDict(
        str_min_length2=2,
        validate_assignment=True
    )
    name: str                       #min 2
    age: int = Field(gt=0, le=120)  #0-120
    email: EmailStr
    is_employed: bool = Field(description='если (is_employed = true), его возраст должен быть от 18 до 65 лет.')
    address: Address

    # # def check_age_employed(cls, value: int, ):
    # #     if value:
    # @field_validator(mode='after')
    # def check_age_employment(self):
    #     if self.is_employed and (self.age < 18 or self.age > 65):
    #         raise ValueError('Работающий пользователь должен быть в возрасте от 18 до 65 лет')
    #     return self

json_data = ["""{   "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }  }""",
"""{   "name": " Jo",
    "age": 13,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New ",
        "street": "5th Avenue",
        "house_number": 1
    }}"""
             ]

# try:
#     user = User.model_validate_json(json_input)
#     print(f"{user.name}, {user.email}, {user.age}, {user.is_employed}")
# except ValidationError as e:
#     print(e)


for data in json_data:
    try:
        user = User.model_validate_json(data)
        print(f"{user.name}, {user.email}, {user.age}, {user.is_employed}")
        print(user.model_dump_json(indent=4))
    except ValidationError as e:
        print(e)