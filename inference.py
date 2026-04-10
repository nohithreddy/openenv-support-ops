import os
import sys
import json
import threading

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ── Required env variables (per OpenEnv checklist) ───────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-api-base-url>")
MODEL_NAME   = os.getenv("MODEL_NAME",   "<your-active-model-name>")
HF_TOKEN     = os.getenv("HF_TOKEN")          # No default – must be injected

from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from env.environment import SupportEnv
from env.models import Action

# ── FastAPI app (serves POST /reset and POST /step for OpenEnv checker) ───────
app = FastAPI(title="SupportOps OpenEnv")

_env = SupportEnv()


class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"


class StepRequest(BaseModel):
    type: str
    ticket_id: int
    message: Optional[str] = None


@app.post("/reset")
def reset(request: ResetRequest):
    task_id = request.task_id or "easy"
    obs = _env.reset(task_id)
    print("START", flush=True)
    return obs.dict()


@app.post("/step")
def step(request: StepRequest):
    action = Action(type=request.type, ticket_id=request.ticket_id, message=request.message)
    obs, reward, done, info = _env.step(action)
    print(f"STEP action={action.type}:{action.ticket_id} reward={reward.score:.3f} done={done}", flush=True)
    if done:
        print("END", flush=True)
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info,
    }


@app.get("/state")
def state():
    return _env.state()


@app.get("/health")
def health():
    return {"status": "ok"}


# ── Agent loop (runs in background thread after server starts) ─────────────────
def run_agent():
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN or "EMPTY",
    )

    SYSTEM_PROMPT = (
        "You are a support ops agent. Given open tickets, pick ONE action as JSON: "
        '{"type": "close"|"escalate"|"reply", "ticket_id": <int>}. '
        "Prioritize urgent/high priority tickets. Respond with valid JSON only."
    )

    def get_llm_action(obs) -> Action:
        ticket_lines = "\n".join(
            f"  id={t.id} priority={t.priority} sla={t.sla} resolved={t.resolved} text={t.text}"
            for t in obs.tickets
        )
        user_msg = (
            f"Tickets:\n{ticket_lines}\n"
            f"Steps: {obs.steps} | Satisfaction: {obs.satisfaction:.2f}\n"
            "Action (JSON only):"
        )
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
            max_tokens=64,
            temperature=0.0,
        )
        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)
        return Action(type=parsed["type"], ticket_id=int(parsed["ticket_id"]))

    env = SupportEnv()

    for task_id in ["easy", "medium", "hard"]:
        print("START", flush=True)
        obs = env.reset(task_id)
        done = False
        step_count = 0

        while not done and step_count < 20:
            try:
                action = get_llm_action(obs)
            except Exception:
                for t in obs.tickets:
                    if not t.resolved:
                        action = Action(type="close", ticket_id=t.id)
                        break

            obs, reward, done, info = env.step(action)
            step_count += 1
            print(f"STEP task={task_id} step={step_count} action={action.type}:{action.ticket_id} reward={reward.score:.3f} done={done}", flush=True)

        print("END", flush=True)


# Start agent in background so FastAPI server can still serve requests
agent_thread = threading.Thread(target=run_agent, daemon=True)
agent_thread.start()