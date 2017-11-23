from SPARQLWrapper import SPARQLWrapper, JSON
import re

f = open('page_links_ru.nt', 'r')


def check_type(search):
    search = search
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbpprop: <http://dbpedia.org/property/>
        ASK {?s rdfs:label "%(search)s"@ru;
                rdf:type foaf:Person }
        """  % locals())
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    res = results['boolean']
    return res


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


result = open('Tolstoy_connections.txt', 'w', encoding='utf-8')

for i in f:
    i = i.encode('utf-8').decode('unicode_escape')
    # print(i)
    res = i.split('>')
    if len(res) == 4:
        if 'Толстой,_Лев_Николаевич' in res[0]:
            person = res[2].split('/')[-1]
            person = re.sub('_', ' ', person)
            if check_type(person):
                name = get_en_name(person)
                # print(person, name)
                if not name:
                    result.write('Tolstoy;' + person + ';\n')
                else:
                    result.write('Tolstoy;' + name + ';\n')

        if 'Толстой,_Лев_Николаевич' in res[2]:
            person = res[0].split('/')[-1]
            person = re.sub('_', ' ', person)
            if check_type(person):
                name = get_en_name(person)
                # print(person, name)
                if not name:
                    result.write(person + ';Tolstoy;\n')
                else:
                    result.write(name + ';Tolstoy;\n')


result.close()
