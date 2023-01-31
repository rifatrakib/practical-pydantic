from pydantic import validate_arguments


@validate_arguments
def pos_or_kw(a: int, b: int = 2) -> str:
    return f"a={a} b={b}"


@validate_arguments
def kw_only(*, a: int, b: int = 2) -> str:
    return f"a={a} b={b}"


@validate_arguments
def pos_only(a: int, b: int = 2, /) -> str:
    return f"a={a} b={b}"


@validate_arguments
def var_args(*args: int) -> str:
    return str(args)


@validate_arguments
def var_kwargs(**kwargs: int) -> str:
    return str(kwargs)


@validate_arguments
def armageddon(
    a: int,
    /,  # python 3.8 only
    b: int,
    c: int = None,
    *d: int,
    e: int,
    f: int = None,
    **g: int,
) -> str:
    return f"a={a} b={b} c={c} d={d} e={e} f={f} g={g}"


print(f"{pos_or_kw(1) = }")
print(f"{pos_or_kw(a=1) = }")
print(f"{pos_or_kw(1, 3) = }")
print(f"{pos_or_kw(a=1, b=3) = }")

print(f"{kw_only(a=1) = }")
print(f"{kw_only(a=1, b=3) = }")

print(f"{pos_only(1) = }")
print(f"{pos_only(1, 2) = }")

print(f"{var_args(1) = }")
print(f"{var_args(1, 2) = }")
print(f"{var_args(1, 2, 3) = }")

print(f"{var_kwargs(a=1) = }")
print(f"{var_kwargs(a=1, b=2) = }")

print(f"{armageddon(1, 2, e=3) = }")
print(f"{armageddon(1, 2, 3, 4, 5, 6, e=8, f=9, g=10, spam=11) = }")
