import unittest


class TestSchema(unittest.TestCase):
    def test_validate():
        from jsonschema import validate
        test_schema = {
            "type": "object",
            "required": ["interaction", "parameters", "new_values"],
            "properties": {
                "interaction": {
                    "type": "string"
                },
                "parameters": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "new_values": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
        test_instance = {
            "interaction": "get",
            "parameters": ["test", "test2"],
            "new_values": ["0", "1"]
        }
        validate(instance=test_instance, schema=test_schema)

    # test_validate()

    def test_update():
        from pprint import pprint

        req_params = ["sub-light", "hyperdrive"]
        request = {"type": "set"}
        for iter in range(len(req_params)):
            request.update({f"param{iter}": req_params[iter]})

        pprint(request, sort_dicts=False)

        test_json = {
            "name": "test"
        }

        test_update = {"parameter": ["param", "value"]}
        test_json.update(test_update)

        # pprint(test_json)
        # print(test_json.keys())
        # print(test_json.values())
        # for item in test_json.values():
        #     print(item)

    # test_update()

    def another_test():
        from jsonschema import validate
        from pprint import pprint

        request = {
            "action": "set",
            "sub-light": "ON",
            "hyperdrive": "OFF"
        }
        set_schema = {
            "type": "object",
            "description": "Schema definition for a SET command",
            "properties": {
                "action": {
                    "type": "string"
                },
                "thrusters": {
                    "type": "string"
                },
                "sub-light": {
                    "type": "string"
                },
                "hyperdrive": {
                    "type": "string"
                },
                "active": {
                    "type": "string"
                },
                "charge": {
                    "type": "string"
                }
            },
            "required": ["action"]
        }
        validate(instance=request, schema=set_schema)
        pprint(set_schema, indent=4, sort_dicts=False)

    another_test()
