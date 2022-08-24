import requests
import pytest

url = 'https://jsonplaceholder.typicode.com'


class TestMain:
    def test_creating_resource(self):
        data = {
            'title': 'Game of Thrones',
            'body': 'Valar Morgulis',
            'userId': 1
        }
        r = requests.post(f'{url}/posts', data)
        assert r.status_code == 201

    def test_updating_resource(self):
        data = {
            'title': 'House of Dragon'
        }
        r = requests.put(f'{url}/posts/1', data)
        assert r.status_code == 200

    def test_delete_resource(self):
        r = requests.delete(f'{url}/posts/1')
        assert r.status_code == 200

    @pytest.mark.parametrize('address, el_s', (('/comments', 500), ('/photos', 5000),
                                               ('/albums', 100), ('/todos', 200), ('/posts', 100), ('/users', 10)))
    def test_get_resource_elements(self, address, el_s):
        r = requests.get(url + address)
        assert r.status_code == 200
        result = r.json()
        assert len(result) == el_s

    @pytest.mark.parametrize('nest', (
            '/posts/1/comments',
            '/albums/1/photos',
            '/users/1/albums',
            '/users/1/todos',
            '/users/1/posts'
    ))
    def test_listing_nested_resources(self, nest):
        r = requests.get(url + nest)
        assert r.status_code == 200
