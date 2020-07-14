import sys
import time
from config import AgentConfig, ValidationError
from application import Application
import os


def get_config() -> AgentConfig:
    try:
        config_file = os.getenv("PAYESHGAR_CONFIG_FILE")
        if config_file is None:
            print("Please set PAYESHGAR_CONFIG_FILE environment variable to a valid Payeshgar config file")
            exit(1)
        return AgentConfig.from_file(config_file)
    except ValidationError as err:
        print("Config file content is not valid for because: {}".format(
            "\n".join(["{}: {}".format(key, value) for key, value in err.detail.items()])
        ))
    except Exception as exp:
        print(str(exp))
    exit(1)


def main():
    agent_config = get_config()
    apps = []
    for server in agent_config.servers:
        app = Application(agent_info=agent_config.agent_info, server_info=server)
        app.run()
        apps.append(app)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for app in apps:
                app.stop()
            sys.exit()


if __name__ == "__main__":
    main()
