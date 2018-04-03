from jinja2 import Environment

from vivo_queries.vdos.organization import Organization


def get_params(connection):
    organization = Organization(connection)
    params = {'Organization': organization}
    return params


def run(connection, **params):

    if params['Organization'].n_number:
        return

    params['upload_url'] = connection.vivo_url

    params['Organization'].n_number = connection.gen_n()

    # template data into q
    q = Environment().from_string("""\
    INSERT DATA {
        GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
        {
            <{{upload_url}}{{Organization.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Organization> .
            <{{upload_url}}{{Organization.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Organization.name}}" . 
        }
    }
    """)

    # Send data to Vivo
    print('=' * 20 + "\nCreating new organization\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    print response
    return response
