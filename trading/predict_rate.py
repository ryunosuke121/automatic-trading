from utils import preprocess


class PredictRateService:
    def __init__(self, model, preprocessing_service: preprocess.PreprocessingService):
        self.model = model
        self.preprocessing_service = preprocessing_service
    
    def predict(self, rate):
        preprocessed_rate = self.preprocessing_service.scale_process(rate)
        prediction = self.model.predict(preprocessed_rate)        
        return prediction
    