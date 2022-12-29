import os
import importlib


def path2module(path):
    return os.path.normpath(path).replace("/", ".")


def check_if_module_correct(src: str) -> bool:
    path = path2module(src)
    return get_setup(path) is not None


def get_all_modules(src: str) -> list[str]:
    result = []
    for file in os.listdir(src):
        path = os.path.join(src, file)
        if os.path.basename(path) == "__pycache__":
            continue
        if os.path.isdir(path):
            result.extend(get_all_modules(path))
        else:
            f = os.path.splitext(path)[0]
            if check_if_module_correct(f):
                result.append(path2module(f))
    return result


def get_setup(module: str):
    try:
        return getattr(importlib.import_module(f"{module}"), "setup")
    except TypeError:
        return None
    except ModuleNotFoundError:
        return None
    except AttributeError:
        return None
