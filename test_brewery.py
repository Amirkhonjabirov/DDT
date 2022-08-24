import requests
import pytest
from jsonschema import validate

url = "https://api.openbrewerydb.org/breweries"

schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'brewery_type': {'type': 'string'},
        'street': {'type': ['string', 'null']},
        'address_2': {'type': ['string', 'null']},
        'address_3': {'type': ['string', 'null']},
        'city': {'type': ['string', 'null']},
        'state': {'type': ['string', 'null']},
        'county_province': {'type': ['string', 'null']},
        'postal_code': {'type': ['string', 'null']},
        'country': {'type': ['string', 'null']},
        'longitude': {'type': ['string', 'null']},
        'latitude': {'type': ['string', 'null']},
        'phone': {'type': ['string', 'null']},
        'website_url': {'type': ['string', 'null']},
        'updated_at': {'type': ['string', 'null']},
        'created_at': {'type': ['string', 'null']},
    },
}


class TestMain:
    def test_single(self):
        obdb_id = '12-gates-brewing-company-williamsville'
        r = requests.get(f"{url}/{obdb_id}")
        result = r.json()
        assert result['id'] == obdb_id
        validate(instance=r.json(), schema=schema)

    def test_by_state(self):
        r = requests.get(f'{url}?by_state=new_york')
        assert r.status_code == 200
        result = r.json()
        for state in result:
            assert state['state'] == 'New York'
            validate(instance=state, schema=schema)

    @pytest.mark.parametrize('req, resp', ((1, 1), (25, 25), (50, 50), (51, 50)))
    def test_per_page(self, req, resp):
        r = requests.get(f'{url}?per_page={req}')
        assert r.status_code == 200
        assert len(r.json()) == resp

    def test_random(self):
        r = requests.get(f'{url}/random')
        result = r.json()
        assert r.status_code == 200
        validate(instance=result[0], schema=schema)

    @pytest.mark.parametrize('search', (('bbq'), ('worcester'), ('stone')))
    def test_search(self, search):
        r = requests.get(f'{url}/search?query={search}')
        assert r.status_code == 200
        result = r.json()
        for research in result:
            validate(instance=research, schema=schema)
