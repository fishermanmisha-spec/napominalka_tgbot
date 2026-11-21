def say_hello():
    print('hello')

say_hello()



def say_hello(name:str='Незнакомец'):
    print('Привет', name)


say_hello('Миша')
say_hello()


def add_numbers(a: float, b: float):
    return a + b


answer = add_numbers(8.6, 565.1)
print(answer)


def boys_age(age: int) -> str:
    if age >= 18:
        return 'Совершеннолетний'
    else:
        return 'несовершеннолетний'


result = boys_age(-100)
print(result)