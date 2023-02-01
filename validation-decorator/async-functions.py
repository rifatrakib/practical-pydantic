import asyncio

from pydantic import PositiveInt, ValidationError, validate_arguments


@validate_arguments
async def get_user_email(user_id: PositiveInt):
    data = {
        1: "test1@abc.com",
        2: "test2@abc.com",
        3: "test3@abc.com",
    }
    email = data.get(user_id, None)
    if email is None:
        raise RuntimeError("user not found")
    else:
        return email


async def main():
    email = await get_user_email(3)
    print(email)
    try:
        await get_user_email(4)
    except ValidationError as exc:
        print(exc.errors())


asyncio.run(main())
