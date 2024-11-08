def decorator(func):
    def wrapper():
        print("Something before the function.")
        func()
        print("Something after the function.")

    return wrapper


@decorator
def greet():
    print("Hello!")


greet()
