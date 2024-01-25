from re import sub
from utils.preprocess import PreprocessingService
from trading.predict_rate import PredictRateService
from load_model import LoadModelService
from rate_publisher import RatePublisher
import queue
from config import get_config
import threading


def main():
    config = get_config()
    model = LoadModelService().load_model("./models/num_model.h5")
    q = RatePublisher(config=config).q
    
    subscribe_thread = threading.Thread(target=subscribe, args=(q, PredictRateService(model).predict))
    subscribe_thread.start()


def subscribe(q: queue.Queue, func):
    while True:
        rate = q.get()
        if rate is None:
            break
        func(rate)
        q.task_done()


if __name__ == "__main__":
    main()
