from unittest import TestCase


class AgentConfigTestCase(TestCase):
    def test_validate_configurations_on_startup_empty_object(self):
        from payeshgar_agent.exceptions import ValidationError
        from payeshgar_agent.initializer import AgentConfig
        case = {}
        with self.assertRaises(ValidationError):
            AgentConfig(case)

    def test_validate_configurations_on_startup_valid_data(self):
        from payeshgar_agent.initializer import AgentConfig
        case = {
            "host_info": {
                "name": "foo",
                "country": "DEU"
            },
            "servers": [
                dict(
                    base_url="http://localhost:8000-",
                    credentials=dict(username='foo', password='bar'),
                    groups=['a', 'b'],
                )
            ]
        }
        sut = AgentConfig(case)
        self.assertEquals(len(sut.servers), 1)
