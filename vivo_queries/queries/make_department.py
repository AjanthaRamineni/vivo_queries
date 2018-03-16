from jinja2 import Environment

from vivo_queries.vdos.department import Department


def get_params(connection):
    department = Department(connection)
    params = {'Department': department}
    return params


def run(connection, **params):
    params['upload_url'] = connection.vivo_url

    params['Department'].n_number = connection.gen_n()
    department_uri = {'Academic department': 'http://vivoweb.org/ontology/core#AcademicDepartment'}
    department_type = department_uri[params['Department'].dep_type]
    params['Department'].dep_type = department_type

    # template data into q
    q = Environment().from_string("""\
    INSERT DATA {
        GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
        {
                <{{upload_url}}{{Department.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .
                <{{upload_url}}{{Department.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{{Department.dep_type}}> .
                <{{upload_url}}{{Department.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label>	"{{Department.name}}" .       
        }
    }
    """)

    # Send data to Vivo
    print('=' * 20 + "\nCreating new department\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response
