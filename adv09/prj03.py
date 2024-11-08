def decorator(func):
    def wrapper(name):
        print("Before the fuction")
        func(name)
        print("After the fuction")

    return wrapper


@decorator
def greet(name):
    print(f"Hello,{name}!")


greet("有的沒的")
