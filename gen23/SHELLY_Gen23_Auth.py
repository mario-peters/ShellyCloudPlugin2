import DomoticzEx as Domoticz
import requests
import json
import hashlib

def extract_data_from_401(response_header: dict[str, str]) -> dict[str, str]:
    """
    Extract data from Shelly 401 response and convert to dict.
    """
    data_401: dict[str, str] = {}
    s = response_header["WWW-Authenticate"]
    s = s.replace("Digest qop", "qop")
    # remove " from values
    s = s.replace('"', "")
    # extract key-value pairs of strings
    for key_value in s.split(", "):
        (key, value) = key_value.split("=")
        data_401[key] = value
    return data_401

def getData_401(URL_SHELLY, username, password, method):
    payload_401 = {
        "id": 1,
        "method": method,
    }
    try:
        data_401:dict[str, str] = {}
        response = requests.post(
            URL_SHELLY,
            timeout=3,
            json=payload_401,
            # data=json.dumps(payload_401),
        )
        if response.status_code == 401:  # noqa: PLR2004
            # print(response.headers)
            data_401 = extract_data_from_401(dict(response.headers))
        #Domoticz.Log(str(data_401))

        response.close()
        return data_401
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def getResponse(data_401, username, password, cnonce):
    auth_parts = [username, data_401["realm"], password]
    # Concatenate the auth_parts with ':' and compute the SHA-256 hash
    ha1 = hashlib.sha256(":".join(auth_parts).encode()).hexdigest()
    ha2 = hashlib.sha256(b"dummy_method:dummy_uri").hexdigest()
    # print(ha1)
    # print(ha2)

    nc = "1"  # number, nonce counter (returned only through websocket channel).
    # It has value of 1 if it is not available in the response

    s = ":".join((ha1, data_401["nonce"], nc, cnonce, "auth", ha2))
    resp = hashlib.sha256(s.encode()).hexdigest()
    return resp
