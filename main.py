from fastapi import FastAPI, Body
from schemas import models as UsageModel
from xml.etree.ElementTree import fromstring

app = FastAPI()


@app.get("/")
async def index():
    return {"api": "fastapi"}


@app.post("/simple-users/", response_model=UsageModel.SimpleUser)
async def read_simple_user(user: UsageModel.SimpleUser):
    return user


@app.post("/users/login/records/", response_model=UsageModel.UserLoginRecord)
async def read_user_login_records(record: UsageModel.UserLoginRecord):
    return record


@app.post("/users/trusted/", response_model=UsageModel.TrustedUser)
async def read_trusted_users(record: UsageModel.TrustedUser):
    user_model = UsageModel.TrustedUser.construct(**record.dict())
    return user_model


@app.post("/recursive-models/", response_model=UsageModel.Spam)
async def read_spam_data(spam: UsageModel.Spam):
    return spam


@app.post("/companies/", response_model=UsageModel.CompanyModel)
async def read_company(company: UsageModel.CompanyModel):
    company_orm = UsageModel.CompanyOrm(**company.dict())
    return company_orm


@app.post("/reserved-keywords/", response_model=UsageModel.ReserveKeyModel)
async def read_keyword(keyword: UsageModel.ReserveKeyModel):
    orm_model = UsageModel.SQLModel(metadata_=keyword.metadata)
    return orm_model


@app.post("/pets/", response_model=UsageModel.Pet)
async def read_pets(pet: UsageModel.Pet):
    pet_orm = UsageModel.PetClass(**pet.dict())
    return pet_orm


@app.post("/persons/", response_model=UsageModel.Person)
async def read_persons(person: UsageModel.Person):
    person_orm = UsageModel.PersonClass(**person.dict())
    pets = []
    for pet in person.pets:
        pets.append(UsageModel.PetClass(**pet.dict()))
    return person_orm


@app.post("/custom-getter-dict/", response_model=UsageModel.UserGetterModel)
async def read_custom_getter(xmlstring: str = Body()):
    user = UsageModel.UserGetterModel.from_orm(fromstring(xmlstring))
    return user


@app.post("/errors/", response_model=UsageModel.Model)
async def read_errors(data: UsageModel.Model):
    return data


@app.post("/validation-errors/", response_model=UsageModel.ValidatorModel)
async def read_invalid_errors(data: UsageModel.ValidatorModel):
    return data


@app.post("/generic-model/", response_model=UsageModel.Response)
async def read_generic_model(data: UsageModel.DataModel):
    return UsageModel.Response[UsageModel.DataModel](data=data)


@app.post("/sub-model/", response_model=UsageModel.ChildModel)
async def read_subclass_model(data: UsageModel.ChildModel):
    return data


@app.post("/model-concrete/", response_model=UsageModel.ResponseConcrete)
async def read_concrete_model(data: UsageModel.ResponseConcrete):
    return data


@app.post("nested/outer/", response_model=UsageModel.OuterT)
async def read_nested_outer_model(data: UsageModel.OuterT):
    return data


@app.post("/models/root/", response_model=UsageModel.RootModel)
async def read_root_model(data: UsageModel.RootModel):
    return data


@app.post("/dynamic-foo-bar/", response_model=UsageModel.DynamicFooBar)
async def read_dynamic_foo_bar_model(data: UsageModel.DynamicFooBar):
    return data


@app.post("/static-foo-bar/", response_model=UsageModel.StaticFooBarModel)
async def read_static_foo_bar_model(data: UsageModel.StaticFooBarModel):
    return data


@app.post("/bar-model/", response_model=UsageModel.BarModel)
async def read_bar_model(data: UsageModel.BarModel):
    return data


@app.post("/dynamic-user/", response_model=UsageModel.DynamicUserModel)
async def read_dynamic_user(data: UsageModel.DynamicUserModel):
    return data


@app.post("/user-from-typed-dict/", response_model=UsageModel.UserTypedDictModel)
async def read_user_typed_dict_model(data: UsageModel.UserTypedDictModel):
    return data


@app.post("/pets-root/", response_model=UsageModel.PetsRoot)
async def read_pets_root(data: UsageModel.PetsRoot):
    return data


@app.post("/pets-root/", response_model=UsageModel.PetsRootName)
async def read_pets_root(data: UsageModel.PetsRootName):
    return data


@app.post("/pets-root/", response_model=UsageModel.CustomizedPet)
async def read_pets_root(data: UsageModel.CustomizedPet):
    return data
