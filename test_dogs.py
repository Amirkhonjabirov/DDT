import requests
import pytest

lst = "https://dog.ceo/api/breeds/list/all"
by_bred = "https://dog.ceo/api/breed"
mult = "https://dog.ceo/api/breeds/image/random"


class TestMain:
    def test_all(self):
        run = requests.get(lst)
        result = run.json()
        var = {"message": dict, "status": str}
        status = result["status"]

        assert run.status_code == 200
        for key, value in var.items():
            assert result.get(key) is not None and isinstance(result[key], value)
        assert status == "success"

    def test_random_by_breed(self, breed='hound'):
        r = requests.get(f'{by_bred}/{breed}/images/random')
        result = r.json()
        assert r.status_code == 200
        assert breed in result["message"]
        assert result['status'] == "success"

    def test_random_by_sub_breed(self, breed='hound', sub='afghan'):
        r = requests.get(f'{by_bred}/{breed}/{sub}/images/random')
        result = r.json()
        assert r.status_code == 200
        assert f"{breed}-{sub}" in result["message"]
        assert result['status'] == "success"

    @pytest.mark.parametrize('req, resp', ((1, 1), (25, 25), (50, 50), (51, 50)))
    def test_random_by_numb_of_breeds(self, req, resp):
        r = requests.get(f'{mult}/{req}')
        result = r.json()
        assert r.status_code == 200
        assert len(result["message"]) == resp
        assert result['status'] == "success"

    @pytest.mark.parametrize('req, resp', ((1, 1), (10, 10), (1001, 1000)))
    def test_random_by_numb_of_breed(self, req, resp):
        r = requests.get(f'{by_bred}/hound/images/random/{req}')
        result = r.json()
        assert r.status_code == 200
        assert len(result["message"]) == resp
