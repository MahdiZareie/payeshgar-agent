import json
import sys
import time
import traceback

from initializer import AgentInitializer
import os


def get_configurations():
    with open(os.getenv("PAYESHGAR_CONFIG_FILE")) as config_file:
        return json.loads(config_file.read())


def main():
    initializer = AgentInitializer(get_configurations())
    agents_list = initializer.initialize()
    del initializer
    for agent in agents_list:
        agent.run()
    while True:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            for agent in agents_list:
                agent.stop()
            sys.exit()
        except Exception as exp:
            print(exp)
            print(traceback)
            sys.exit(1)


if __name__ == "__main__":
    main()
