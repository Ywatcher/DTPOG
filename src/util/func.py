from inspect import signature
from typing import Callable


def n_args(f: Callable) -> int:
    sig = signature(f)
    return len(dict(sig.parameters))
