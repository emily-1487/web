def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)
        print("After the function")
        return result

    return wrapper


@decorator
def greet(name=None):
    if name:
        print(f"Hello,{name}!")
    else:
        print("Hello!")


greet()
greet("有的沒的")
