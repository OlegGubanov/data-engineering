with open('text_2_var_66', 'r') as file:
    with open('result_2_var_66', 'w') as result:
        for line in file:
            numbers = line.split(':')
            numbers_sum = sum([int(number) for number in numbers])
            result.write(str(numbers_sum) + '\n')
