import logging
import time
from typing import Any, Callable, Tuple

logger = logging.getLogger("graph_pipeline")
handler = logging.FileHandler("errors.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


def timer(
        func: Callable[..., Tuple[Any, float]]
) -> Callable[..., Tuple[Any, float]]:
    def wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], (int, float)):
            return result
        return result, elapsed
    return wrapper
