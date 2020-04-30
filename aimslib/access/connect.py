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


def _check_response(r: requests.Response, *args, **kwargs) -> None:
    """Checks the response from a request; raises exceptions as required."""
    r.raise_for_status()


def _login(
        session: requests.Session,
        server_url:str,
        username:str,
        password:str,
        recurse: bool = True
) -> str:
    """Logs on to the AIMS server, handling retry if requred.

    :param session: requests Session object to use for logon.
    :param server_url: Url of the AIMS server.
    :param username: Registered username of user.
    :param password: Password of user.
    :param recurse: Used to allow a single recursion for retry. Do not use.

    :returns: The base url for accessing other pages.

    :raises: requests exceptions.
    """
    encoded_id = base64.b64encode(username.encode()).decode()
    encoded_pw = hashlib.md5(password.encode()).hexdigest()
    r = session.post(server_url,
                     {"Crew_Id": encoded_id, "Crm": encoded_pw},
                     timeout=REQUEST_TIMEOUT)
    base_url = r.url.split("wtouch.exe")[0]
    #If already logged in, need to logout then login again
    if r.text.find("Please log out and try again.") != -1:
        if not recurse: raise AT.LogonError
        logout(session, base_url)
        base_url = _login(session, server_url, username, password, False)
    if r.text.find("Please re-enter your Credentials and try again") != -1:
        raise AT.UsernamePasswordError
    return base_url


def connect(server_url: str, username:str, password:str
) -> T.Tuple[requests.Session, str]:
    """Connects to AIMS server.

    :param server_url: The url of the AIMS server to connect to
    :param username: Registered username of user
    :param password: Password of user

    :return: Tuple of form (session object, base url)

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
    url =_login(session, server_url, username, password)
    return (session, url.split("wtouch.exe")[0])


def logout(session: requests.Session, base_url: str) -> None:
    """Logout of the AIMS server.

    :param session: The session object returned from connect.
    :param base_url: The base url returned from connect.

    :return: None
    """
    session.post(base_url + "perinfo.exe/AjAction?LOGOUT=1",
                 {"AjaxOperation": "0"},
                 timeout=REQUEST_TIMEOUT)


def changes(session: requests.Session, base_url: str) -> bool:
    """Check for changes notification.

    :param session: The session object returned from connect.
    :param base_url: The base url returned from connect.

    :return: True if change notification was detected, else False
    """
    r = session.get(base_url + "perinfo.exe/index",
                    timeout=REQUEST_TIMEOUT)
    no_changes_marker = '\r\nvar notification = Trim("");\r\n'
    return  True if r.text.find(no_changes_marker) == -1 else False
