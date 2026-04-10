from typing import Tuple, Dict
from .models import Observation, Action, Reward, Ticket
from .tasks import TASKS
import random


class SupportEnv:

    def __init__(self, seed=42):
        random.seed(seed)
        self.max_steps = 15

    def reset(self, task_type="easy") -> Observation:
        task = TASKS[task_type]

        self.state_data = {
            "tickets": [
                {**t, "resolved": False} for t in task["tickets"]
            ],
            "steps": 0,
            "satisfaction": 1.0,
        }

        return self._get_obs()

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
        self.state_data["steps"] += 1
        reward = 0.0

        for t in self.state_data["tickets"]:
            if t["id"] == action.ticket_id and not t["resolved"]:
                if action.type == "close":
                    t["resolved"] = True
                    reward += 0.4
                elif action.type == "escalate":
                    reward -= 0.2

        for t in self.state_data["tickets"]:
            if not t["resolved"]:
                t["sla"] -= 1
                if t["sla"] < 0:
                    reward -= 0.3
                    self.state_data["satisfaction"] -= 0.1

        done = (
            all(t["resolved"] for t in self.state_data["tickets"])
            or self.state_data["steps"] >= self.max_steps
        )

        reward = max(min(reward, 1.0), -1.0)

        return (
            self._get_obs(),
            Reward(score=reward, feedback="dense reward"),
            done,
            {}
        )

    def state(self):
        return self.state_data

    def _get_obs(self):
        return Observation(
            tickets=[Ticket(**t) for t in self.state_data["tickets"]],
            steps=self.state_data["steps"],
            satisfaction=self.state_data["satisfaction"]
        )