import re

from pydantic import BaseModel, ValidationError

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
