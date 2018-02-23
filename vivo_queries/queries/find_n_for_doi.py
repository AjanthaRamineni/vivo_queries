from vivo_queries.vdos.thing import Thing

def get_params(connection):
    thing = Thing (connection)
    params = {'Thing': thing,}
    return params

def get_query(**params):
    query = """SELECT ?uri ?doi WHERE {{?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle> . ?uri <http://purl.org/ontology/bibo/doi> ?doi . FILTER (regex (?doi, "{}")) }}""".format(params['Thing'].name)

    return query
    
def run(connection, **params):
    q = get_query(connection, **params)

    print('=' * 20 + "\nFinding n number\n" + '=' * 20)
    response = connection.run_query(q)

    data = response.json()
    matches = {}
    for listing in data['results']['bindings']:
        doi = parse_json(listing, 'doi')
        url = parse_json(listing, 'uri')
        url_n = url.rsplit('/', 1)[-1]
        matches[url_n] = doi

    return matches

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value