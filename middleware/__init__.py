from functools import wraps


class Middleware:
    def __init__(self, callback=None, is_async=True, is_class_method=False):
        self.callback = callback
        self.is_async = is_async
        self.is_class_method = is_class_method

    def __call__(self, func):
        if self.is_class_method:
            if self.is_async:
                return self.__create_class_async_method_middleware()(func)
            return self.__create_class_sync_method_middleware()(func)
        if self.is_async:
            return self.__create_async_middleware()(func)
        return self.__create_sync_middleware()(func)

    def hook(self, **kwargs):
        """
        Decorator to create a middleware hook.
        """

        def wrap_func(func):
            if self.is_class_method:
                if self.is_async:
                    return self.__create_class_async_method_middleware(**kwargs)(func)
                return self.__create_class_sync_method_middleware(**kwargs)(func)
            if self.is_async:
                return self.__create_async_middleware(**kwargs)(func)
            return self.__create_sync_middleware(**kwargs)(func)

        return wrap_func

    def __create_async_middleware(self, **kwargs):
        """
        Create an async middleware wrapper for a given function.
        """
        callback = self.callback
        func_keys = kwargs

        def wrap_func(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                res = await callback(*args, **{**kwargs, **func_keys})
                if isinstance(res, dict):
                    for key, value in res.items():
                        kwargs[key] = value
                return await func(*args, **kwargs)

            return wrapper

        return wrap_func

    def __create_sync_middleware(self, **kwargs):
        """
        Sync middlewares.
        """
        callback = self.callback

        def wrap_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                res = callback(*args, **kwargs)
                if isinstance(res, dict):
                    for key, value in res.items():
                        kwargs[key] = value
                return func(*args, **kwargs)

            return wrapper

        return wrap_func

    def __create_class_sync_method_middleware(self, **kwargs):
        """
        Create a class method middleware.
        """
        callback = self.callback

        def wrap_func(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                res = callback(self, *args, **kwargs)
                if isinstance(res, dict):
                    kwargs.update(res)
                return func(self, *args, **kwargs)

            return wrapper

        return wrap_func

    def __create_class_async_method_middleware(self, **kwargs):
        """
        Create a class method middleware.
        """
        callback = self.callback

        def wrap_func(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                res = await callback(*args, **kwargs)
                if isinstance(res, dict):
                    for key, value in res.items():
                        kwargs[key] = value
                return await func(*args, **kwargs)

            return wrapper

        return wrap_func


def remove_keys(**kwargs):
    """
    Remove keys from the kwargs.
    """
    keys = kwargs.get("keys", [])

    def wrap_func(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for key in keys:
                if kwargs.get(key):
                    del kwargs[key]
            return await func(*args, **kwargs)

        return wrapper

    return wrap_func
