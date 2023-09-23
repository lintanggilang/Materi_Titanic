from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model = pickle.load(open('model.sav', 'rb'))

def umur(x):
    if x <= 12:
        return "1"
    elif x >= 13 and x <= 18:
        return "2"
    elif x >= 19 and x <= 40:
        return "3"
    elif x >= 41 and x <= 65:
        return "4"    
    else:
        return "5"

class Passenger(BaseModel):
    Pclass: int = Field(example=3)
    Sex: str = Field(example="male")
    Age: float = Field(example=22.0)
    SibSp: int = Field(example=1)
    Parch: int = Field(example=0)
    Fare: float = Field(example=7.25)
    Embarked: str = Field(example="S")

@app.get("/")
def read_root():
    return {"Hello": "Titanic"}

@app.post("/Titanic/")
def predict_survival(passenger: Passenger):
    try:
        # Create DataFrame
        df = pd.DataFrame([dict(passenger)])

        # Apply the 'umur' function
        df['umur'] = df['Age'].apply(lambda x : umur(x))
        df['WA'] = 0
        df.loc[(df['umur'] == '1') | (df['Sex'] == 'female'), 'WA'] = 1

        # Predict
        prediction = model.predict(df)
        result = {"Survived": int(prediction[0])}
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
