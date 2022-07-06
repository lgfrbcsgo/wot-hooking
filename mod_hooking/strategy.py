from mod_hooking.hooking import hooking_strategy
from mod_hooking.logging import LOG_CURRENT_EXCEPTION


@hooking_strategy
def override(orig_func, func, *args, **kwargs):
    try:
        return func(orig_func, *args, **kwargs)
    except Exception:
        LOG_CURRENT_EXCEPTION()
        return orig_func(*args, **kwargs)


@hooking_strategy
def after(orig_func, func, *args, **kwargs):
    result = orig_func(*args, **kwargs)
    try:
        func(result, *args, **kwargs)
    except Exception:
        LOG_CURRENT_EXCEPTION()
    finally:
        return result


@hooking_strategy
def before(orig_func, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception:
        LOG_CURRENT_EXCEPTION()
    finally:
        return orig_func(*args, **kwargs)
