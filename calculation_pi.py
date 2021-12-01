def calc_pi(n_terms: int):
    numerator: float = 4.0
    denominator: float = 1.0
    operation: float = 1.0
    result = numerator / denominator

    for n in range(n_terms):
        operation *= -1.0
        denominator += 2.0
        result += operation * (numerator / denominator)

    return result

if __name__ == "__main__":
    n = 100000000
    print(calc_pi(n))
