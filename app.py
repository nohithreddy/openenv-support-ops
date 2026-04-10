from fastapi import FastAPI
from env.environment import SupportEnv

app = FastAPI()
env = SupportEnv()

@app.get("/")
def run():
    obs = env.reset("medium")
    return {"observation": obs.dict()}