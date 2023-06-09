import inspect

import js
from pyodide.ffi.wrappers import add_event_listener


def when(event_type=None, selector=None):
    """
    Decorates a function and passes py-* events to the decorated function
    The events might or not be an argument of the decorated function
    """

    def decorator(func):
        elements = js.document.querySelectorAll(selector)
        sig = inspect.signature(func)
        # Function doesn't receive events
        if not sig.parameters:

            def wrapper(*args, **kwargs):
                func()

            for el in elements:
                add_event_listener(el, event_type, wrapper)
        else:
            for el in elements:
                add_event_listener(el, event_type, func)
        return func

    return decorator
