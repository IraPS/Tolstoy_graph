from transliterate import translit
import re

r = open('Tolstoy_graph_v2.txt', 'r', encoding='utf-8')
w = open('Tolstoy_graph_v2.csv', 'w', encoding='utf-8')

w.write('Source;Target;Weight;In index\n')

for i in r:
    i = re.sub('Tolstoy', 'Leo Tolstoy', i)
    i = re.sub(';н\n', ';1\n', i)
    i = re.sub(';д\n', ';10\n', i)
    try:
        name = i.split(';')[0]
        surname = name.split(',')[0]
        other_name = name.split(',')[1]
        new_name = surname + other_name
        transl_name = (translit(new_name, reversed=True))
        i = re.sub(name, transl_name, i)
        w.write(i)
    except:
        try:
            name = i.split(';')[1]
            surname = name.split(',')[0]
            other_name = name.split(',')[1]
            new_name = surname + other_name
            transl_name = (translit(new_name, reversed=True))
            i = re.sub(name, transl_name, i)
            w.write(i)
        except:
            w.write(i)

w.close()
