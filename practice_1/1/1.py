with open('text_1_var_66', 'r') as file:
    words_dict = {}
    for line in file:
        line = (line.replace(',', ' ')
                .replace('.', ' ')
                .replace('?', ' ')
                .replace('!', ' '))
        words = line.split()
        for word in words:
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1

result = dict(sorted(words_dict.items(), key=lambda item: item[1], reverse=True))
with open('result_1_var_66.txt', 'w') as result_file:
    for key,value in result.items():
        result_file.write(f"{key}:{value}\n")
