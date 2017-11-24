from SPARQLWrapper import SPARQLWrapper, JSON
import re


def get_en_name(search):
    search = search
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbpprop: <http://dbpedia.org/property/>
        SELECT DISTINCT ?e ?name
        WHERE {
	        ?e rdfs:label "%(search)s"@ru .
                ?e dbp:name ?name
              }
        """ % locals())
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        res = results[u'results']
    except:
        print("""
        PREFIX dbpprop: <http://dbpedia.org/property/>
        SELECT DISTINCT ?e ?name
        WHERE {
	        ?e rdfs:label "%(search)s"@ru .
                ?e dbp:name ?name
              }
        """ % locals())
    # print(res)
    try:
        res = res[u'bindings'][0]
        name = res['name']['value']
    except:
        name = False
    return name


links = open('tolstoy_links.txt', 'r', encoding='utf-8')
connections = open('Tolstoy_connections.txt', 'w', encoding='utf-8')
for link in links:
    link = link.split('>')
    if 'Толстой,_Лев_Николаевич' in link[0]:
        entity = link[2].split('/')[-1]
        if ',' in entity and 'фильм' not in entity:
            person = re.sub('_', ' ', entity)
            name = get_en_name(person)
            # print(person, name)
            if not name:
                connections.write('Tolstoy;' + person + ';\n')
            else:
                connections.write('Tolstoy;' + name + ';\n')
        else:
            pass
            # if '_' in entity: print(entity)
    if 'Толстой,_Лев_Николаевич' in link[2]:
        entity = link[0].split('/')[-1]
        if ',' in entity and 'фильм' not in entity:
            person = re.sub('_', ' ', entity)
            name = get_en_name(person)
            # print(person, name)
            if not name:
                connections.write(person + ';Tolstoy;\n')
            else:
                connections.write(name + ';Tolstoy;\n')
        else:
            pass
            # if '_' in entity: print(entity)


connections.close()
