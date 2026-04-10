from fastapi import FastAPI
from env.environment import SupportEnv

app = FastAPI()

env = SupportEnv()


@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}


@app.post("/step")
def step(action: dict):
    next_state, reward, done, info = env.step(action)
    return {
        "state": next_state,
        "reward": reward,
        "done": done,
        "info": info
    }