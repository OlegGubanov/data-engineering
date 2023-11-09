import math


def filter_number(number: str):
    if math.sqrt(float(number)) >= 50 + 66:
        return number


with open('text_3_var_66', 'r') as file:
    with open('result_3_var_66', 'w') as result:
        for line in file:
            numbers = line.strip().split(',')
            for i in range(len(numbers)):
                if numbers[i] == "NA":
                    numbers[i] = str((int(numbers[i - 1]) + int(numbers[i + 1])) / 2)
            numbers = list(filter(lambda item: item is not None, [filter_number(number) for number in numbers]))
            result.write(','.join(numbers) + '\n')
