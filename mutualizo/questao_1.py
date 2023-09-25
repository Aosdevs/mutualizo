def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Exemplo de uso:
n = 10  # Substitua 10 pelo número desejado
resultado = fibonacci(n)
print(f"O {n}-ésimo termo da sequência de Fibonacci é {resultado}")
