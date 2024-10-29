#!/usr/bin/env python

"""
Test basic kepler functions
"""
import unittest
import pathlib
import threading as th
import queue
import time

import rain
import rain.client
import rain.defaults
import rain.server
import rain.trigger
import rain.packaging


SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"


class TestPubServer(unittest.TestCase):

    def test_start_stop_pub_server(self):
        self.test_server = rain.defaults.Server("pub", [])
        self.test_server.publ_host = "127.0.0.1"
        self.test_server.publ_port = 8000
        self.test_server.trig_host = "127.0.0.1"
        self.test_server.trig_port = 8001

        self.paths = rain.defaults.Paths(
            SERVER_CONFIG_LOC / "authorised_keys",
            SERVER_CONFIG_LOC / "keypairs",
            SERVER_CONFIG_LOC / "plugins"
        )

        self.queue = queue.Queue()
        self.exit_magic = (rain.server.SERVER_EXIT_KEY, rain.server.SERVER_EXIT_CODE)

        server = th.Thread(
            target=rain.server.run_publish,
            args=(
                self.test_server,
                self.paths
            ),
            kwargs={
                "custom_message_queue": self.queue,
            },
        )
        server.start()
        self.queue.put(self.exit_magic)
        server.join()


class TestSubClientTowardsServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_server = rain.defaults.Server("pub", [])
        cls.test_server.publ_host = "127.0.0.1"
        cls.test_server.publ_port = 8000
        cls.test_server.trig_host = "127.0.0.1"
        cls.test_server.trig_port = 8001

        cls.paths = rain.defaults.Paths(
            SERVER_CONFIG_LOC / "authorised_keys",
            SERVER_CONFIG_LOC / "keypairs",
            SERVER_CONFIG_LOC / "plugins"
        )

        cls.test_client = rain.defaults.Client("reindeer", "sub", 10000)
        cls.test_client.hostname = "127.0.0.1"
        cls.test_client.port = 8000

        cls.client_paths = rain.defaults.Paths(
            SERVER_CONFIG_LOC / "known_hosts",
            SERVER_CONFIG_LOC / "keypairs",
            None
        )

        rain.load_plugins(SERVER_CONFIG_LOC / "plugins")

        cls.queue = queue.Queue()
        cls.exit_magic = (rain.server.SERVER_EXIT_KEY, rain.server.SERVER_EXIT_CODE)

        cls.server = th.Thread(
            target=rain.server.run_publish,
            args=(
                cls.test_server,
                cls.paths
            ),
            kwargs={
                "custom_message_queue": cls.queue,
            },
        )
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.queue.put(cls.exit_magic)
        cls.server.join()

    def test_sub_one_timed_param(self):
        response_generator = rain.client.run_subscribe(
            client=self.test_client,
            params=["activity"],
            paths=self.client_paths
        )

        response = next(response_generator)
        assert response["action"] == "sub", response
        assert response["name"] == "activity", response
        assert response["data"] == "grazing", response

        response = next(response_generator)
        assert response["action"] == "sub", response
        assert response["name"] == "activity", response
        assert response["data"] == "grazing", response

    def test_trigger_wrong_param(self):
        trigger_response = rain.trigger.send_trigger(
            server_host=self.test_server.trig_host,
            server_port=self.test_server.trig_port,
            name="activity",
            value="DANCING",
        )
        assert trigger_response["name"] == "activity", trigger_response
        assert trigger_response["data"] == rain.server.SERVER_TRIGGER_REQ_FAIL, trigger_response

    def test_trigger(self):
        trigger_response = rain.trigger.send_trigger(
            server_host=self.test_server.trig_host,
            server_port=self.test_server.trig_port,
            name="antlers",
            value="They fell off!",
        )
        assert trigger_response["name"] == "antlers", trigger_response
        assert trigger_response["data"] == rain.server.SERVER_TRIGGER_REQ_OK, trigger_response

    def test_sub_one_trigger(self):
        response_generator = rain.client.run_subscribe(
            client=self.test_client,
            params=["antlers"],
            paths=self.client_paths
        )
        local_q = queue.Queue()

        def launch_subscribe():
            response = next(response_generator)
            local_q.put(response)

        send_trigger = th.Thread(
            target=launch_subscribe,
        )
        send_trigger.start()
        time.sleep(0.01)

        trigger_response = rain.trigger.send_trigger(
            server_host=self.test_server.trig_host,
            server_port=self.test_server.trig_port,
            name="antlers",
            value="They fell off!",
        )
        assert trigger_response["name"] == "antlers", trigger_response
        assert trigger_response["data"] == rain.defaults.SERVER_TRIGGER_REQ_OK, trigger_response

        send_trigger.join()
        response = local_q.get()

        assert response["action"] == "sub", response
        assert response["name"] == "antlers", response
        assert response["data"] == "They fell off!", response
