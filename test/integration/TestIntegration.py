import unittest
import pycurl
import re
import json
import pytest

from io import BytesIO
from urllib.parse import urlencode

itemid = ""
texttranlate = ""

@pytest.fixture()
def urlaws(pytestconfig):
    url = "https://"+pytestconfig.getoption("gateway")+".execute-api.us-east-1.amazonaws.com/Prod/todos"
    return url

@pytest.mark.dependency()
def test_insert(urlaws):
    print(urlaws)
    curl = pycurl.Curl()
    b_obj = BytesIO()
    curl.setopt(pycurl.URL, urlaws)
    curl.setopt(curl.WRITEDATA, b_obj)
    curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
    request = json.dumps({"text": "Learn python and more" })
    curl.setopt(curl.POSTFIELDS, request)
    curl.perform()
    code = curl.getinfo(pycurl.HTTP_CODE)
    curl.close()
    get_body = b_obj.getvalue()
    response = json.loads(get_body.decode('utf8'))


    if code == 200:
        global itemid
        itemid = response["id"]
        pass
    else:
        assert 0

@pytest.mark.dependency(depends=["test_insert"])
def test_get(urlaws):
    curl = pycurl.Curl()
    b_obj = BytesIO()
    global itemid
    url = urlaws+'/'+itemid
    curl.setopt(pycurl.URL, url)
    curl.setopt(curl.WRITEDATA, b_obj)
    curl.perform()
    code = curl.getinfo(pycurl.HTTP_CODE)
    curl.close()
    get_body = b_obj.getvalue()
    response = json.loads(get_body.decode('utf8'))

    if code == 200:
        pass
    else:
        assert 0

@pytest.mark.dependency(depends=["test_insert"])
def test_list(urlaws):
    curl = pycurl.Curl()
    b_obj = BytesIO()
    curl.setopt(pycurl.URL, urlaws)
    curl.setopt(curl.WRITEDATA, b_obj)
    curl.perform()
    code = curl.getinfo(pycurl.HTTP_CODE)
    curl.close()
    get_body = b_obj.getvalue()
    response = json.loads(get_body.decode('utf8'))

    if code == 200 and len(response) > 0 and any(x["id"] == itemid for x in response) :
        pass
    else:
        assert 0

@pytest.mark.dependency(depends=["test_insert"])
def test_trnaslate(urlaws):
    curl = pycurl.Curl()
    b_obj = BytesIO()

    global itemid
    url = urlaws+'/'+itemid+"/es"
    curl.setopt(pycurl.URL, url)
    curl.setopt(curl.WRITEDATA, b_obj)
    curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
    curl.perform()
    code = curl.getinfo(pycurl.HTTP_CODE)
    curl.close()
    get_body = b_obj.getvalue()
    response = json.loads(get_body.decode('utf8'))

    if code == 200 and response["text"] == "Aprender python y más":
        global texttranlate
        texttranlate = response["text"]
        pass
    else:
        assert 0

@pytest.mark.dependency(depends=["test_insert", "test_trnaslate"])
def test_update(urlaws):
    curl = pycurl.Curl()
    b_obj = BytesIO()

    global itemid
    url = urlaws+'/'+itemid

    curl.setopt(pycurl.URL, url)
    curl.setopt(curl.WRITEDATA, b_obj)
    curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
    global texttranlate
    request = json.dumps({ "text": texttranlate, "checked": True })
    curl.setopt(curl.POSTFIELDS, request)
    curl.setopt(pycurl.CUSTOMREQUEST, "PUT")
    curl.perform()
    code = curl.getinfo(pycurl.HTTP_CODE)
    curl.close()
    get_body = b_obj.getvalue()
    response = json.loads(get_body.decode('utf8'))

    if code == 200:
        pass
    else:
        assert 0

@pytest.mark.dependency(depends=["test_insert", "test_update"])
def test_delete(urlaws):
    curl = pycurl.Curl()
    b_obj = BytesIO()

    global itemid
    url = urlaws+'/'+itemid
    curl.setopt(pycurl.URL, url)
    curl.setopt(curl.WRITEDATA, b_obj)
    curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
    curl.setopt(pycurl.CUSTOMREQUEST, "DELETE")
    curl.perform()
    code = curl.getinfo(pycurl.HTTP_CODE)
    curl.close()

    if code == 200:
        pass
    else:
        assert 0


