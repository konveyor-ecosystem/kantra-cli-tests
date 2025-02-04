import base64
import binascii
import hashlib
import os
import re

from lxml import etree
from Crypto.Cipher import AES
from urllib.request import urlopen
from utils import constants


def manage_credentials_in_maven_xml(path, reset=False):
    """
    Purpose of this function is to add/remove git user data from maven file allowing analysis to get access to git repo
    Args:
        path: path to the XML configuration file
        reset: when False - credentials will be read from env variables and written to the file, if True - they will be removed from the file.

    Returns: void

    """
    tree = etree.parse(path)
    root = tree.getroot()

    namespaces = {'mvn': 'http://maven.apache.org/SETTINGS/1.2.0'}

    if not reset:
        username = os.getenv(constants.GIT_USERNAME)
        password = os.getenv(constants.GIT_PASSWORD)
    else:
        username = ''
        password = ''

    for server in root.xpath('//mvn:server', namespaces=namespaces):
        username_elem = server.find('mvn:username', namespaces)
        password_elem = server.find('mvn:password', namespaces)

        if username_elem is not None:
            username_elem.text = username
        if password_elem is not None:
            password_elem.text = password

    tree.write(path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def get_default_token():
    try:
        # Fallback method to try get default maven token from go-konveyor-tests repo source
        key = hashlib.sha256(b"k0nv3y0r.io").digest()
        src = urlopen("https://raw.githubusercontent.com/konveyor/go-konveyor-tests/refs/heads/main/analysis/analysis_test.go").read()
        crypted_token = re.findall(r'DecodeString\("([a-f0-9]+)"', str(src))[0]

        enc = binascii.unhexlify(crypted_token)
        nonce = enc[:12]
        ciphertext = enc[12:-16]
        tag = enc[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)

        return decrypted.decode()
    except Exception as e:
        print("Get default token failed, error:", e)
        return ''
