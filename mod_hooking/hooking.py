import inspect
import sys
from functools import update_wrapper, wraps


class Hook(object):
    def __init__(self, strategy, orig_func, func):
        update_wrapper(self, orig_func)
        self.strategy = strategy
        self.orig_func = orig_func
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.strategy(self.orig_func, self.func, *args, **kwargs)

    def __get__(self, instance, cls):
        @wraps(self.orig_func)
        def bound(*args, **kwargs):
            return self(instance, *args, **kwargs)

        return bound


def hook(strategy, module, func_name, func):
    strategy(module, func_name)(func)


def unhook(module, func_name, strategy=None, func=None):
    first = None
    previous = None
    orig_func = getattr(module, func_name)

    while isinstance(orig_func, Hook):
        if (orig_func.func != func and func is not None) or (
            orig_func.strategy != strategy and strategy is not None
        ):
            previous = orig_func
            if first is None:
                first = orig_func

        elif previous is not None:
            previous.orig_func = orig_func.orig_func

        orig_func = orig_func.orig_func

    monkey_patch(module, func_name, first or orig_func)


def monkey_patch(module, func_name, func):
    if inspect.ismodule(module):
        setattr(sys.modules[module.__name__], func_name, func)
    elif inspect.isclass(module):
        setattr(module, func_name, func)


def hooking_strategy(strategy_func):
    def build_decorator(module, func_name):
        def decorator(func):
            orig_func = getattr(module, func_name)
            patch = Hook(strategy_func, orig_func, func)
            monkey_patch(module, func_name, patch)
            return func

        return decorator

    return build_decorator
