#!/usr/bin/env python

"""
Test of the top-level functions for running a Request Client and a Response
server
"""
import unittest
import pathlib
import threading as th

import rain
import rain.client
import rain.defaults
import rain.server
import rain.packaging


SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"


class TestRepServer(unittest.TestCase):

    def test_start_stop_rep_server(self):
        self.test_server = rain.defaults.Server("rep", [])
        self.test_server.publ_host = "127.0.0.1"
        self.test_server.publ_port = 8000
        self.test_server.trig_host = None
        self.test_server.trig_port = None

        self.paths = rain.defaults.Paths(
            SERVER_CONFIG_LOC / "authorised_keys",
            SERVER_CONFIG_LOC / "keypairs",
            SERVER_CONFIG_LOC / "plugins"
        )

        self.server_running = True
        server = th.Thread(
            target=rain.server.run_response,
            args=(
                self.test_server,
                self.paths
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
        cls.test_server = rain.defaults.Server("rep", [])
        cls.test_server.publ_host = "127.0.0.1"
        cls.test_server.publ_port = 8000
        cls.test_server.trig_host = None
        cls.test_server.trig_port = None

        cls.server_paths = rain.defaults.Paths(
            SERVER_CONFIG_LOC / "authorised_keys",
            SERVER_CONFIG_LOC / "keypairs",
            SERVER_CONFIG_LOC / "plugins"
        )

        cls.test_get_client = rain.defaults.Client("reindeer", "get", 1000)
        cls.test_get_client.hostname = "127.0.0.1"
        cls.test_get_client.port = 8000

        cls.test_set_client = rain.defaults.Client("reindeer", "set", 1000)
        cls.test_set_client.hostname = "127.0.0.1"
        cls.test_set_client.port = 8000

        cls.client_paths = rain.defaults.Paths(
            SERVER_CONFIG_LOC / "known_hosts",
            SERVER_CONFIG_LOC / "keypairs",
            None
        )

        rain.load_plugins(cls.server_paths.plugins)

        cls.server_running = True
        cls.server = th.Thread(
            target=rain.server.run_response,
            args=(
                cls.test_server,
                cls.server_paths
            ),
            kwargs={
                "exit_handler": lambda: cls.server_running,
            },
        )
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server_running = False
        cls.server.join()

    def test_get_wrong_param(self):
        response_generator = rain.client.run_request(
            client=self.test_get_client,
            params=["what_they_doin"],
            data=None,
            paths=self.client_paths
        )
        response = next(response_generator)
        assert response["data"][0] == rain.defaults.NO_SUCH_PARAM_ERROR.format("what_they_doin"), response

    def test_get_one_param(self):
        response_generator = rain.client.run_request(
            client=self.test_get_client,
            params=["activity"],
            data=None,
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "get", response
        assert response["name"][0] == "activity", response
        assert response["data"][0] == "grazing", response

    def test_get_two_params(self):
        response_generator = rain.client.run_request(
            client=self.test_get_client,
            params=["herd_size", "activity"],
            data=None,
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "get", response
        assert response["name"][0] == "herd_size", response
        assert response["data"][0] == "10", response
        assert response["name"][1] == "activity", response
        assert response["data"][1] == "grazing", response

    def test_set_one_param(self):
        response_generator = rain.client.run_request(
            client=self.test_set_client,
            params=["activity"],
            data=["sleeping"],
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "set", response
        assert response["name"][0] == "activity", response

        # Run a `get` command to verify the `set` command worked
        response_generator = rain.client.run_request(
            client=self.test_get_client,
            params=["activity"],
            data=None,
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "get", response
        assert response["name"][0] == "activity", response
        assert response["data"][0] == "sleeping", response

        # Set the modified value back to its default
        response_generator = rain.client.run_request(
            client=self.test_set_client,
            params=["activity"],
            data=["grazing"],
            paths=self.client_paths
        )
        response = next(response_generator)

    def test_set_two_params(self):
        response_generator = rain.client.run_request(
            client=self.test_set_client,
            params=["herd_size", "activity"],
            data=["14", "sleeping"],
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "set", response
        assert response["name"][0] == "herd_size", response
        assert response["name"][1] == "activity", response

        # Run a `get` command to verify the `set` command worked
        response_generator = rain.client.run_request(
            client=self.test_get_client,
            params=["herd_size", "activity"],
            data=None,
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "get", response
        assert response["name"][0] == "herd_size", response
        assert response["data"][0] == "14", response
        assert response["name"][1] == "activity", response
        assert response["data"][1] == "sleeping", response

        # Set the modified values back to their defaults
        response_generator = rain.client.run_request(
            client=self.test_set_client,
            params=["herd_size", "activity"],
            data=["10", "grazing"],
            paths=self.client_paths
        )
        response = next(response_generator)
