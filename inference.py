import asyncio
import os
from typing import List, Optional

from openai import OpenAI
from env.environment import SupportEnv


# ================== CONFIG ==================
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY") or "dummy"
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASK_NAME = "support-env-task"
BENCHMARK = "support-env"
MAX_STEPS = 10


# ================== LOGGING ==================
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True
    )


# ================== MAIN ==================
async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = SupportEnv()

    rewards = []
    steps_taken = 0
    success = False
    score = 0.0  # IMPORTANT FIX

    log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

    try:
        state = env.reset()   # your env returns Observation object

        for step in range(1, MAX_STEPS + 1):

            # FIX: access tickets properly
            tickets = state.tickets

            unresolved = [t for t in tickets if not t.resolved]

            if not unresolved:
                done = True
                break

            ticket_id = unresolved[0].id

            # create proper Action object
            from env.models import Action
            action = Action(type="close", ticket_id=ticket_id)

            next_state, reward, done, info = env.step(action)

            rewards.append(reward.score if hasattr(reward, "score") else reward)
            steps_taken = step

            log_step(
                step=step,
                action=f"close({ticket_id})",
                reward=rewards[-1],
                done=done,
                error=None
            )

            state = next_state

            if done:
                break

        # normalize score
        score = min(max(sum(rewards) / len(rewards), 0.0), 1.0) if rewards else 0.0
        success = score > 0.1

    except Exception as e:
        log_step(step=steps_taken + 1, action="error", reward=0.0, done=True, error=str(e))

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())