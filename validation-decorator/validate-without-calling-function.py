from pydantic import ValidationError, validate_arguments


@validate_arguments
def slow_sum(a: int, b: int) -> int:
    print(f"Called with a={a}, b={b}")
    return a + b


print(f"{slow_sum(1, 1) = }")
print(f"{slow_sum.validate(2, 2) = }")

try:
    m = slow_sum.validate(1, "b")
except ValidationError as exc:
    print(exc)
