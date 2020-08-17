import json

from falcon import testing
import pytest

from main import app

CREATES_POLYGON_IDS = []
POLYGON_DATA = {
                    "name": "test",
                    "class_id": 12213,
                    "props": {
                        "test": "test"
                    },
                    "geom": [
                           [0, 1], [2, 2], [2, 1], [0, 1]
                    ]
                }


@pytest.fixture
def client():
    return testing.TestClient(app)


def test_post(client):
    polygon = dict(POLYGON_DATA)
    res = client.simulate_post(
        '/polygon',
        body=json.dumps(polygon),
        headers={'content-type': 'application/json'}
    )
    CREATES_POLYGON_IDS.append(res.json['id'])
    res_data = res.json
    assert res_data['geom'][0] == polygon['geom']
    assert res_data['props'] == polygon['props']


def test_list(client):
    res = client.simulate_get(
        '/polygon',
    )
    assert len(res.json) > 0
    assert res.json[0]['id'] == CREATES_POLYGON_IDS[0]


def test_detail(client):
    res = client.simulate_get(f'/polygon/{CREATES_POLYGON_IDS[0]}')
    assert res.json['id'] == CREATES_POLYGON_IDS[0]
    assert res.json['props'] == POLYGON_DATA['props']
    assert res.json['class_id'] == POLYGON_DATA['class_id']
    assert res.json['name'] == POLYGON_DATA['name']
    assert res.json['geom'][0] == POLYGON_DATA['geom']


def test_update(client):
    data = dict(POLYGON_DATA)
    data.update({'geom': [[0, 1], [3, 3], [3, 2], [0, 1]]})
    res = client.simulate_patch(
            f'/polygon/{CREATES_POLYGON_IDS[0]}',
            body=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
    assert res.json['geom'][0] == data['geom']


def test_delete(client):
    res = []
    for _id in CREATES_POLYGON_IDS:
        res.append(client.simulate_delete(f'/polygon/{_id}'))

    for r in res:
        assert r.status == '204 No Content'
