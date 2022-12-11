import re
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError
from pydantic.fields import ModelField

AgedType = TypeVar("AgedType")
QualityType = TypeVar("QualityType")

# https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
post_code_regex = re.compile(
    r"(?:"
    r"([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?"
    r"([0-9][A-Z]{2})|"
    r"(BFPO) ?([0-9]{1,4})|"
    r"(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|"
    r"([A-Z]{2}) ?([0-9]{2})|"
    r"(GE) ?(CX)|"
    r"(GIR) ?(0A{2})|"
    r"(SAN) ?(TA1)"
    r")"
)


class PostCode(str):
    """Partial UK postcode validation.

    Note: this is just an example, and is not
    intended for use in production; in particular this does NOT guarantee
    a postcode exists, just that it has a valid format.
    """

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        m = post_code_regex.fullmatch(v.upper())
        if not m:
            raise ValueError("invalid postcode format")
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(f"{m.group(1)} {m.group(2)}")

    def __repr__(self):
        return f"PostCode({super().__repr__()})"


class TastingModel(Generic[AgedType, QualityType]):
    def __init__(self, name: str, aged: AgedType, quality: QualityType):
        self.name = name
        self.aged = aged
        self.quality = quality

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField):
        if not isinstance(v, cls):
            raise TypeError("invalid value")
        if not field.sub_fields:
            return v

        aged_f = field.sub_fields[0]
        quality_f = field.sub_fields[1]
        errors = []

        valid_value, error = aged_f.validate(v.aged, {}, loc="aged")
        if error:
            errors.append(error)

        valid_value, error = quality_f.validate(v.quality, {}, loc="quality")
        if error:
            errors.append(error)

        if errors:
            raise ValidationError(errors, cls)
        return v


class Pet:
    def __init__(self, name: str):
        self.name = name


class Model(BaseModel):
    post_code: PostCode


class PetOwner(BaseModel):
    pet: Pet
    owner: str

    class Config:
        arbitrary_types_allowed = True


class Tasting(BaseModel):
    # for wine, "aged" is an int with years, "quality" is a float
    wine: TastingModel[int, float]
    # for cheese, "aged" is a bool, "quality" is a str
    cheese: TastingModel[bool, str]
    # for thing, "aged" is a Any, "quality" is Any
    thing: TastingModel


model = Model(post_code="sw8 5el")
print(f"{model = }")
print(f"{model.post_code = }")

print(f"{Model.schema() = }")

pet = Pet(name="Hedwig")
m = PetOwner(owner="Harry", pet=pet)
print(f"{m = }")
print(f"{m.pet = }")
print(f"{m.pet.name = }")
print(f"{type(m.pet) = }")

try:
    m = PetOwner(owner="Harry", pet="Hedwig")
    print(m)
except ValidationError as e:
    print(e)

pet = Pet(name=42)
m = PetOwner(owner="Harry", pet=pet)
print(f"{m = }")
print(f"{m.pet = }")
print(f"{m.pet.name = }")
print(f"{type(m.pet) = }")

model = Tasting(
    # This wine was aged for 20 years and has a quality of 85.6
    wine=TastingModel(name="Cabernet Sauvignon", aged=20, quality=85.6),
    # This cheese is aged (is mature) and has "Good" quality
    cheese=TastingModel(name="Gouda", aged=True, quality="Good"),
    # This Python thing has aged "Not much" and has a quality "Awesome"
    thing=TastingModel(name="Python", aged="Not much", quality="Awesome"),
)

print(f"{model = }")
print(f"{model.wine.aged = }")
print(f"{model.wine.quality = }")
print(f"{model.cheese.aged = }")
print(f"{model.cheese.quality = }")
print(f"{model.thing.aged = }")

try:
    m = Tasting(
        # For wine, aged should be an int with the years, and quality a float
        wine=TastingModel(name="Merlot", aged=True, quality="Kinda good"),
        # For cheese, aged should be a bool, and quality a str
        cheese=TastingModel(name="Gouda", aged="yeah", quality=5),
        # For thing, no type parameters are declared, and we skipped validation
        # in those cases in the Assessment.validate() function
        thing=TastingModel(name="Python", aged="Not much", quality="Awesome"),
    )
except ValidationError as e:
    print(e)
