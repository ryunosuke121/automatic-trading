from re import sub
from turtle import pu
from utils.preprocess import PreprocessingService
from predict_rate import PredictRateService
from load_model import LoadModelService
from rate_publisher import RatePublisher
import queue
from config import get_config
import threading
from log_config import logger
import logging

def main():
    logger.info("start trading")
    config = get_config()
    model = LoadModelService().load_model(config["model_path"])
    preprocessing_service = PreprocessingService(
        window_size=config["window_size"], predict_min_after=config["predict_min_after"]
    )
    rate_publisher = RatePublisher(config=config)
    
    subscribe_thread = threading.Thread(
        target=subscribe, args=(rate_publisher.q, PredictRateService(model, preprocessing_service).predict)
    )
    subscribe_thread.start()
    
    publish_thread = threading.Thread(target=rate_publisher.run, args=())
    
    publish_thread.start()


def subscribe(q: queue.Queue, func):
    while True:
        rate = q.get()
        if rate is None:
            break
        func(rate)
        q.task_done()


if __name__ == "__main__":
    main()
