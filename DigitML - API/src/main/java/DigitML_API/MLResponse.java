package DigitML_API;

public class MLResponse {
    private String prediction;
    
    public String getPrediction() {
        return prediction;
    }
    
    public void setPrediction(String prediction) {
        this.prediction = prediction;
    }
    
    @Override
    public String toString() {
        return "MLResponse [prediction=" + prediction + "]";
    }
}
