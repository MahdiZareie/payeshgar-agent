import sys
import time
from config import AgentConfig
from application import Application


def main():
    config_file = sys.argv[1]
    agent_config = AgentConfig.from_file(config_file)
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
