from collections import Counter

graph = open('Tolstoy_graph.csv', 'w', encoding='utf-8')
graph.write('Source;Target;Weight;\n')

connections = open('Tolstoy_connections.txt', 'r', encoding='utf-8')
connections = Counter(connections)

for con in connections:
    print(con)
    graph.write(con.split('\n')[0] + str(connections[con]) + ';\n')

graph.close()