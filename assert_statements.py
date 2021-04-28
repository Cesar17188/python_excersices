def divisors(num):

    divisors = [i for i in range(1, num+1) if num % i == 0]
    return divisors


def run():
    num = input("Ingresa un número: ")
    assert num.isnumeric() and int(num) >= 0, 'Debes ingresar un número positivo'
    print(divisors(int(num)))
    print("terminó mi programa")


if __name__ == '__main__':
    run()
