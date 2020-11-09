from gym.envs.registration import register

register(
    id='chase-v0',
    entry_point='gym_chase.envs:ChaseEnv',
)

register(
    id='chase-mental-v0',
    entry_point='gym_chase.envs:MentalChaseEnv',
)