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


@app.post("/user/login/records/", response_model=UsageModel.UserLoginRecord)
async def read_user_login_records(record: UsageModel.UserLoginRecord):
    return record


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
