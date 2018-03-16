from jinja2 import Environment

from vivo_queries.vdos.author import Author
from vivo_queries.vdos.contributor import Contributor


def get_params(connection):
    author = Author(connection)
    contributor = Contributor(connection)
    params = {'Contributor': contributor, 'Author': author}
    return params


def run(connection, **params):
    params['upload_url'] = connection.vivo_url
    params['Contributor'].n_number = connection.gen_n()
    contributor_role_uri = {'Co-Principal Investigator Role': 'http://vivoweb.org/ontology/core#CoPrincipalInvestigatorRole',
                            'Investigator Role': 'TBD',
                            'Researcher Role': 'TBD',
                            'Principal Investigator Role': 'TBD'}
    contributor_role_type = contributor_role_uri[params['Contributor'].type]
    params['Contributor'].type = contributor_role_type
    params['Contributor'].person_id = params['Author'].n_number

    # template data into q
    q = Environment().from_string("""\
        INSERT DATA {
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> 
            {
                <{{upload_url}}{{Author.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Contributor.name}}"^^<http://www.w3.org/2001/XMLSchema#string> .
                <{{upload_url}}{{Contributor.n_number}}> <http://purl.obolibrary.org/obo/ARG_2000028> <{{upload_url}}{{Author.vcard}}> .
                <{{upload_url}}{{Contributor.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053> <{{upload_url}}{{Author.name_id}}> . 
        }
        """)

    # send data to vivo
    print('=' * 20 + "\nAdding contributor\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response
