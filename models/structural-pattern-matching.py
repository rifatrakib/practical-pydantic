from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    species: str


a = Pet(name="Bones", species="dog")

# MUST HAVE Python 3.10 or above
match a:
    # match `species` to "dog", declare and initialize `dog_name`
    case Pet(species="dog", name=dog_name):
        print(f"{dog_name} is a dog")
    # default case
    case _:
        print("No dogs matched")
