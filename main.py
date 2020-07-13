import os
import sys
import time

from application import Application


def main():
    app = Application()
    app.run()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            app.stop()
            sys.exit()


if __name__ == "__main__":
    main()
