from pydantic import BaseModel, Field


class Voice(BaseModel):
    name: str = Field(None, alias="ActorName")
    language_code: str = None
    mood: str = None


class Character(Voice):
    act: int = 1

    class Config:
        fields = {"language_code": "lang"}

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return "".join(word.capitalize() for word in string.split("_"))


print(f"{Character.schema(by_alias=True) = }")
