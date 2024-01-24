import animate
import threading
import websocket
import json
from matplotlib import pyplot as plt
from get_rate import GatherDataWebSocketService
import signal
import sys


def signal_handler(sig, frame):
    print("Signal received: ", sig)
    if gatherDataWebSocketService.ws:
        gatherDataWebSocketService.ws.close()
    sys.exit(0)


def main():
    global gatherDataWebSocketService
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        visualizer = animate.RealtimeFXVisualizer()
        gatherDataWebSocketService = GatherDataWebSocketService(visualizer)
        thread = threading.Thread(target=gatherDataWebSocketService.run)
        thread.start()
        plt.show()
    except:
        if gatherDataWebSocketService.ws:
            gatherDataWebSocketService.ws.close()


if __name__ == "__main__":
    main()
