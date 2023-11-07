from response_generator import generate_response


def start_test():
    requests = {
        "Найди документ со словом год": ['Cколько-домашней-кошке-«человеческих»-лет.pdf',
                                         'Программисты-уже-не-в-моде.pdf',
                                         'Самая-загадочная-бизнес-империя-мира.pdf',
                                         'Четверо-злоумышленников-украли-кости-динозавров.pdf'],
        "Какие документы содержат слово кошка": ['Cколько-домашней-кошке-«человеческих»-лет.pdf']
    }

    global_a = 0
    global_b = 0
    global_c = 0
    global_d = 0
    score_list = []
    for request, relevant in requests.items():
        result = []
        a = 0
        b = 0
        c = 0
        d = 0
        r = 0
        p = 0
        accurancy = 0
        e = 0
        f = 0
        finded = generate_response(request)
        print(finded, 'finded')
        for item in finded:
            result.append(item[38:].split('\n')[0])
        print(result, 'res')
        print(relevant, 'rel')
        for item1 in result:
            if item1 in relevant:
                a += 1
                global_a += 1
            else:
                b += 1
                global_b += 1
        for item2 in relevant:
            if item2 not in result:
                c += 1
                global_c += 1
        d = 5 - (a + c)
        global_d += d
        r = a / (a + c)
        p = a / (a + b)
        accurancy = (a + d) / (a + b + c + d)
        e = (b + c) / (a + b + c + d)
        f = 2 / (1 / p + 1 / r)
        score_list.append({'r': r, 'p': p, 'a': accurancy, 'e': e, 'f': f})
    print(score_list)
    print(global_a / (global_a + global_c))
    i = 0
    average_r = 0
    average_p = 0
    average_a = 0
    average_e = 0
    average_f = 0
    for score in score_list:
        i += 1
        average_r += score['r']
        average_p += score['p']
        average_a += score['a']
        average_e += score['e']
        average_f += score['f']
    average_r = average_r / i
    average_p = average_p / i
    average_a = average_a / i
    average_e = average_e / i
    average_f = average_f / i
    global_r = global_a / (global_a + global_c)
    global_p = global_a / (global_a + global_b)
    global_accurancy = (global_a + global_d) / (global_a + global_b + global_c + global_d)
    global_e = (global_b + global_c) / (global_a + global_b + global_c + global_d)
    global_F = 2 / (1 / global_p + 1 / global_r)
    answer = f'''
    Microaverage:
    recall = {average_r}
    precision = {average_p}
    accurancy = {average_a}
    error = {average_e}
    F-measure = {average_f}
    Macroaverage:
    recall = {global_r}
    precision = {global_p}
    accurancy = {global_accurancy}
    error = {global_e}
    F-measure = {global_F}
    '''
    print(answer)
    return answer


if __name__ == '__main__':
    start_test()
