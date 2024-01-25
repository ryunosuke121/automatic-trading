import os

def get_config():
    config = {
        "symbol": os.getenv("SYMBOL"),
        "window_size": int(os.getenv("WINDOW_SIZE")),
        "predict_min_after": int(os.getenv("PREDICT_MIN_AFTER")),
    }
    
    return config