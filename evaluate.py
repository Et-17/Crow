import setup

def get_time_and_coeffs(julian_day, subdivisions):
    for key in subdivisions.keys():
        if key[0] < julian_day and key[1] > julian_day:
            return ((julian_day - key[0]) / (key[1] - key[0]), subdivisions[key])

def compute_chebyshev(time, coeffs):
    polys = []
    polys.append(1)
    polys.append(time)

    for i in range(2, len(coeffs)):
        polys.append(2 * time * polys[i - 1] - polys[i - 2])
    
    result = 0
    for i in range(len(coeffs)):
        result += coeffs[i] * polys[i]
    
    return result

def test():
    subdivisions = setup.setup()
    for day in range(2460472, 2461472):
        (time, coeffs) = get_time_and_coeffs(day, subdivisions)
        x = compute_chebyshev(time, coeffs[0])
        y = compute_chebyshev(time, coeffs[1])
        z = compute_chebyshev(time, coeffs[2])
        print(f"{x}, {y}, {z}")

test()
