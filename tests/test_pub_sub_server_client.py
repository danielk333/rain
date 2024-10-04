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
import rain.server
import rain.trigger
import rain.packaging


SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"


class TestPubServer(unittest.TestCase):

    def test_run_publish(self):
        self.queue = queue.Queue()
        self.exit_magic = (rain.server.SERVER_EXIT_KEY, rain.server.SERVER_EXIT_CODE)
        server = th.Thread(
            target=rain.server.run_publish,
            args=(
                ("localhost", 8000),
                ("localhost", 8001),
                [],
                SERVER_CONFIG_LOC / "authorised_keys",
                SERVER_CONFIG_LOC / "keypairs",
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
        rain.load_plugins(SERVER_CONFIG_LOC / "plugins")

        cls.queue = queue.Queue()
        cls.exit_magic = (rain.server.SERVER_EXIT_KEY, rain.server.SERVER_EXIT_CODE)
        cls.server_address = ("localhost", 8000)
        cls.trigger_address = ("localhost", 8001)
        cls.server = th.Thread(
            target=rain.server.run_publish,
            args=(
                cls.server_address,
                cls.trigger_address,
                [],
                SERVER_CONFIG_LOC / "authorised_keys",
                SERVER_CONFIG_LOC / "keypairs",
            ),
            kwargs={
                "custom_message_queue": cls.queue,
            },
        )
        cls.server.start()

        cls.client_kwargs = dict(
            server="reindeer",
            server_address=cls.server_address,
            timeouts=[10000, 10000],
            path_pub=SERVER_CONFIG_LOC / "known_hosts",
            path_prv=SERVER_CONFIG_LOC / "keypairs",
        )

    @classmethod
    def tearDownClass(cls):
        cls.queue.put(cls.exit_magic)
        cls.server.join()

    def test_run_client_sub(self):
        response_generator = rain.client.run_subscribe(
            params=["activity"],
            **self.client_kwargs
        )
        response = next(response_generator)
        assert response["action"] == "sub", response
        assert response["name"] == "activity", response
        assert response["data"] == "grazing", response

        response = next(response_generator)
        assert response["action"] == "sub", response
        assert response["name"] == "activity", response
        assert response["data"] == "grazing", response

    def test_trigger_non_trigger_fail(self):
        trigger_response = rain.trigger.send_trigger(
            server_host=self.trigger_address[0],
            server_port=self.trigger_address[1],
            name="activity",
            value="DANCING",
        )
        assert trigger_response["name"] == "activity", trigger_response
        assert trigger_response["data"] == rain.server.SERVER_TRIGGER_REQ_FAIL, trigger_response

    def test_trigger(self):
        trigger_response = rain.trigger.send_trigger(
            server_host=self.trigger_address[0],
            server_port=self.trigger_address[1],
            name="antlers",
            value="They fell off!",
        )
        assert trigger_response["name"] == "antlers", trigger_response
        assert trigger_response["data"] == rain.server.SERVER_TRIGGER_REQ_OK, trigger_response

    def test_run_client_sub_trigger(self):
        response_generator = rain.client.run_subscribe(
            params=["antlers"],
            **self.client_kwargs
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
            server_host=self.trigger_address[0],
            server_port=self.trigger_address[1],
            name="antlers",
            value="They fell off!",
        )
        assert trigger_response["name"] == "antlers", trigger_response
        assert trigger_response["data"] == rain.server.SERVER_TRIGGER_REQ_OK, trigger_response

        send_trigger.join()
        response = local_q.get()

        assert response["action"] == "sub", response
        assert response["name"] == "antlers", response
        assert response["data"] == "They fell off!", response
