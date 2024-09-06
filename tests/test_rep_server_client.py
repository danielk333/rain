#!/usr/bin/env python

"""
Test basic kepler functions
"""
import time
import unittest
import subprocess
import pathlib
import json

SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"
REP_SERVER_COMMAND = [
    "rain-server", "rep",
    "-c", str(SERVER_CONFIG_LOC),
    "--loglevel", "DEBUG",
    "--printlevel", "DEBUG",
    "--logprint",
]
REQ_CLIENT_COMMAND = [
    "rain-client", "reindeer",
    "-c", str(SERVER_CONFIG_LOC),
    "--loglevel", "DEBUG",
    "--printlevel", "DEBUG",
    "--logprint",
]
REQ_SILENT_CLIENT_COMMAND = [
    "rain-client", "reindeer",
    "-c", str(SERVER_CONFIG_LOC),
    "--loglevel", "ERROR",
    "--printlevel", "ERROR",
]
DELTA_T_SEC = 0.5


class TestRunRepServer(unittest.TestCase):

    def test_run_server(self):
        print(" ".join(REP_SERVER_COMMAND))
        server_proc = subprocess.Popen(REP_SERVER_COMMAND)
        time.sleep(DELTA_T_SEC)
        server_proc.terminate()
        time.sleep(DELTA_T_SEC)
        ret_status = server_proc.poll()
        assert ret_status == -15, "Server did not return KeyboardInteruppt"

    def test_run_server_args_error(self):
        print(" ".join(REP_SERVER_COMMAND))
        server_proc = subprocess.Popen(REP_SERVER_COMMAND + ["--fake-arg"])
        time.sleep(DELTA_T_SEC)
        server_proc.terminate()
        time.sleep(DELTA_T_SEC)
        ret_status = server_proc.poll()
        assert ret_status == 2, "Server did not return argument fail"


class TestRunRepClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(" ".join(REP_SERVER_COMMAND))
        cls.server_proc = subprocess.Popen(REP_SERVER_COMMAND)
        time.sleep(DELTA_T_SEC)

    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()
        time.sleep(DELTA_T_SEC)
        ret_status = cls.server_proc.poll()
        assert ret_status == -15, "Server did not return KeyboardInteruppt"

    def test_run_client_get(self):
        cmd = REQ_CLIENT_COMMAND + ["get", "activity"]
        print(" ".join(cmd))
        subprocess.check_call(cmd)

    def test_run_client_get_args_error(self):
        cmd = REQ_CLIENT_COMMAND + ["fake-arg",]
        print(" ".join(cmd))
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_call(cmd)


class TestRepServerMessages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(" ".join(REP_SERVER_COMMAND))
        cls.server_proc = subprocess.Popen(REP_SERVER_COMMAND)
        time.sleep(DELTA_T_SEC)

    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()
        time.sleep(DELTA_T_SEC)
        ret_status = cls.server_proc.poll()
        assert ret_status == -15, "Server did not return KeyboardInteruppt"

    def test_run_client_get(self):
        cmd = REQ_SILENT_CLIENT_COMMAND + ["get", "activity"]
        print(" ".join(cmd))
        ret = subprocess.check_output(cmd)
        ret = json.loads(ret.decode())
        assert ret["data"][0] == "grazing", ret

    def test_run_client_get_wrong(self):
        cmd = REQ_SILENT_CLIENT_COMMAND + ["get", "what_they_doin"]
        print(" ".join(cmd))
        ret = subprocess.check_output(cmd)
        ret = json.loads(ret.decode())
        assert ret["data"][0].endswith("invalid"), ret
