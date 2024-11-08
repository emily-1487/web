def decorator_with_args(greeting):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"{greeting}! Before the function")
            result = func(*args, **kwargs)
            print(f"{greeting}!After the function")
            return result

        return wrapper

    return decorator


@decorator_with_args("Hi")
def greet(name=None):
    if name:
        print(f"Hello,{name}!")
    else:
        print(f"Hello!")


greet()
greet("有的沒的")
