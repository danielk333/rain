#!/usr/bin/env python

"""
Test basic kepler functions
"""
import unittest
import pathlib
import threading as th

import rain
import rain.client
import rain.server
import rain.packaging


SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"


class TestRepServer(unittest.TestCase):

    def test_run_response(self):
        self.server_running = True
        server = th.Thread(
            target=rain.server.run_response,
            args=(
                ("localhost", 8000),
                [],
                SERVER_CONFIG_LOC / "authorised_keys",
                SERVER_CONFIG_LOC / "keypairs",
            ),
            kwargs={
                "exit_handler": lambda: self.server_running,
            },
        )
        server.start()
        self.server_running = False
        server.join()


class TestRepClientTowardsServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rain.load_plugins(SERVER_CONFIG_LOC / "plugins")

        cls.server_running = True
        cls.server_address = ("localhost", 8000)
        cls.server = th.Thread(
            target=rain.server.run_response,
            args=(
                cls.server_address,
                [],
                SERVER_CONFIG_LOC / "authorised_keys",
                SERVER_CONFIG_LOC / "keypairs",
            ),
            kwargs={
                "exit_handler": lambda: cls.server_running,
            },
        )
        cls.server.start()

        cls.client_kwargs = dict(
            server="reindeer",
            server_address=cls.server_address,
            timeouts=[1000, 1000],
            path_pub=SERVER_CONFIG_LOC / "known_hosts",
            path_prv=SERVER_CONFIG_LOC / "keypairs",
        )

    @classmethod
    def tearDownClass(cls):
        cls.server_running = False
        cls.server.join()

    def test_run_client_get(self):
        response_generator = rain.client.run_request(
            action="get",
            params=["activity"],
            data=None,
            **self.client_kwargs
        )
        response = next(response_generator)
        assert response["action"] == "get", response
        assert response["name"][0] == "activity", response
        assert response["data"][0] == "grazing", response

    def test_run_client_get_non_existant(self):
        response_generator = rain.client.run_request(
            action="get",
            params=["what_they_doin"],
            data=None,
            **self.client_kwargs
        )
        response = next(response_generator)
        assert response["data"][0] == rain.packaging.NO_SUCH_PARAM_ERROR.format("what_they_doin"), response
