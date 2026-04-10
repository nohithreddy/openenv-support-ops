import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ── Required env variables (per OpenEnv checklist) ──────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-api-base-url>")
MODEL_NAME   = os.getenv("MODEL_NAME",   "<your-active-model-name>")
HF_TOKEN     = os.getenv("HF_TOKEN")          # No default – must be injected

from openai import OpenAI
from env.environment import SupportEnv
from env.models import Action

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN or "EMPTY",
)

SYSTEM_PROMPT = """You are a support operations agent. You will receive a list of open tickets.
For each step, you must decide on exactly ONE action in JSON format:
{"type": "close"|"escalate"|"reply", "ticket_id": <int>}
Prioritize urgent and high-priority tickets first. Always respond with valid JSON only."""


def get_llm_action(obs) -> Action:
    """Ask the LLM to choose an action given the current observation."""
    ticket_lines = "\n".join(
        f"  id={t.id} priority={t.priority} sla={t.sla} resolved={t.resolved} text={t.text}"
        for t in obs.tickets
    )
    user_msg = (
        f"Current tickets:\n{ticket_lines}\n"
        f"Steps taken: {obs.steps} | Customer satisfaction: {obs.satisfaction:.2f}\n"
        "Choose the best action (JSON only):"
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

    import json
    raw = response.choices[0].message.content.strip()
    parsed = json.loads(raw)
    return Action(type=parsed["type"], ticket_id=int(parsed["ticket_id"]))


def main():
    env = SupportEnv()

    for task_id in ["easy", "medium", "hard"]:
        print("START")                          # Required log marker

        obs = env.reset(task_id)
        done = False
        step_count = 0

        while not done and step_count < 20:
            try:
                action = get_llm_action(obs)
            except Exception as e:
                # Fallback: close the first unresolved ticket
                for t in obs.tickets:
                    if not t.resolved:
                        action = Action(type="close", ticket_id=t.id)
                        break

            obs, reward, done, info = env.step(action)
            step_count += 1

            print("STEP",                       # Required log marker
                  f"task={task_id}",
                  f"step={step_count}",
                  f"action={action.type}:{action.ticket_id}",
                  f"reward={reward.score:.3f}",
                  f"done={done}")

        print("END")                            # Required log marker


if __name__ == "__main__":
    main()