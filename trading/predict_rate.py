

class PredictRateService:
    def __init__(self, model):
        self.model = model
    
    def predict(self, rate):
        prediction = self.model.predict(rate)
        print(prediction)
        return prediction
    