#!/usr/bin/python3
"""
This module provides basic functions for access to AIMS server:

connect - for connecting to an AIMS server
logout - for logging out of an AIMS server
changes - for checking for changes notification
"""

import typing as T
import requests
import base64
import hashlib
import os

import aimslib.common.types as AT


REQUEST_TIMEOUT = os.getenv("AIMS_TIMEOUT") or 60

PostFunc = T.Callable[[str, T.Dict[str, str]], requests.Response]
HeartbeatFunc = T.Optional[T.Callable[[], None]]

def _check_response(r: requests.Response, *args, **kwargs) -> None:
    """Checks the response from a request; raises exceptions as required."""
    r.raise_for_status()


def _login(
        session: requests.Session,
        server_url:str,
        enc_username:str,
        enc_password:str,
        heartbeat: HeartbeatFunc,
        recurse: bool = True
) -> PostFunc:
    """Logs on to the AIMS server, handling retry if requred.

    :param session: requests Session object to use for logon.
    :param server_url: Url of the AIMS server.
    :param username: Registered username of user.
    :param password: Password of user.
    :param heartbeat: Function called by post closure
    :param recurse: Used to allow a single recursion for retry. Do not use.

    :returns: Function to be called to POST to AIMS

    :raises: requests exceptions.
    """
    r = session.post(server_url,
                     {"Crew_Id": enc_username, "Crm": enc_password},
                     timeout=REQUEST_TIMEOUT)
    if heartbeat: heartbeat()
    base_url = r.url.split("wtouch.exe")[0]
    def post(rel_url: str, data: T.Dict[str, str]) -> requests.Response:
        url = base_url + rel_url
        if "useGET" in data.keys():
            del data["useGET"]
            r = session.get(url, params=data, timeout=REQUEST_TIMEOUT)
        else:
            r = session.post(url, data=data, timeout=REQUEST_TIMEOUT)
        if heartbeat: heartbeat()
        return r
    retval: PostFunc = post
    #If already logged in, need to logout then login again
    if r.text.find("Please log out and try again.") != -1:
        if not recurse: raise AT.LogonError
        logout(post)
        retval = _login(session, server_url, enc_username, enc_password, heartbeat, False)
    if r.text.find("Please re-enter your Credentials and try again") != -1:
        raise AT.UsernamePasswordError
    return retval


def connect(server_url: str, username:str, pw:str, hb: HeartbeatFunc = None
) -> PostFunc:
    """Connects to AIMS server.

    :param server_url: The url of the AIMS server to connect to
    :param username: Registered username of user
    :param pw: Password of user

    :return: Function to be called to send requests to AIMS. This function has the form
        post(relative_url, data_dictionary). If data_dictionary has a "useGET" as a key,
        a GET request without data will be sent, otherwise it will be a POST request.

    :raises requests.ConnectionError: A network problem occured.
    :raises requests.HTTPError: Request returned unsuccessful status code.
    :raises requests.Timeout: No response from server within
        REQUEST_TIMEOUT seconds.

    Mimics the sign of procedure that a web browser would use to sign on to
    the ecrew server. The returned session and base url allow access to other
    AIMS pages.
    """
    session = requests.Session()
    session.hooks['response'].append(_check_response)
    session.headers.update({
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) "
        "Gecko/20100101 Firefox/64.0"})
    encoded_id = base64.b64encode(username.encode()).decode()
    encoded_pw = hashlib.md5(pw.encode()).hexdigest()
    post_func = _login(session, server_url, encoded_id, encoded_pw, hb)
    del pw #for ease of auditing
    return post_func


def logout(post: PostFunc) -> None:
    """Logout of the AIMS server.

    :param session: The session object returned from connect.
    :param base_url: The base url returned from connect.

    :return: None
    """
    post("perinfo.exe/AjAction?LOGOUT=1", {"AjaxOperation": "0"})


def changes(post: PostFunc) -> bool:
    """Check for changes notification.

    :param session: The session object returned from connect.
    :param base_url: The base url returned from connect.

    :return: True if change notification was detected, else False
    """
    r = post("perinfo.exe/index", {"useGet": "1"})
    no_changes_marker = '\r\nvar notification = Trim("");\r\n'
    return  True if r.text.find(no_changes_marker) == -1 else False
