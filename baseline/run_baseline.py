from env.environment import SupportEnv
from env.models import Action
from env.grader import grade

env = SupportEnv(seed=42)
obs = env.reset("hard")

done = False

while not done:
    for t in obs.tickets:
        if not t.resolved:
            action = Action(type="close", ticket_id=t.id)
            break

    obs, reward, done, _ = env.step(action)

print("Final Score:", grade(env.state()))