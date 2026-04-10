import os
from env.environment import SupportEnv

# Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "local")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline")
HF_TOKEN = os.getenv("HF_TOKEN")

print("START")

env = SupportEnv()
state = env.reset()

done = False
step_count = 0

while not done and step_count < 20:
    action = {"action": "resolve"}  # simple baseline action

    next_state, reward, done, info = env.step(action)

    print(f"STEP {step_count}")
    print(f"State: {next_state}")
    print(f"Reward: {reward}")
    print(f"Done: {done}")

    state = next_state
    step_count += 1

print("END")