from pydantic import BaseModel, ByteSize


class Model(BaseModel):
    size: ByteSize


print(f"{Model(size=52000).size = }")
print(f"{Model(size='3000 KiB').size = }")

m = Model(size="50 PB")
print(f"{m.size.human_readable() = }")
print(f"{m.size.human_readable(decimal=True) = }")
print(f"{m.size.to('TiB') = }")
