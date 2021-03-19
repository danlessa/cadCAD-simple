
from typing import *

Variables = NamedTuple
Parameters = NamedTuple
Substep = int
Timestep = int
SubstepHistory = List[Variables]
History = List[SubstepHistory]
Results = List[History]


VariableUpdate = Callable[[Parameters, Substep, History, Variables], Variables]
SubstepBlock = List[VariableUpdate]
TimestepBlock = List[SubstepBlock]


def update_state(substep_block: SubstepBlock,
                 params: Parameters,
                 substep: Substep,
                 history: History,
                 state: Variables) -> Variables:

    temp_state = state.copy()
    for _, variable_fn in substep_block:
        temp_state = variable_fn(params, substep, history, temp_state)
    return temp_state

def run_simulation(initial_state: Variables,
                   params: Parameters,
                   timestep_block: TimestepBlock,
                   timesteps: Timestep,
                   samples: int) -> Results:
    results: Results = []
    for _ in range(samples):
        state: Variables = initial_state.copy()
        history: History = []
        for _ in range(timesteps):
            substep_history: SubstepHistory = []
            for (substep, substep_block) in enumerate(timestep_block):
                state = update_state(substep_block,
                                     params,
                                     substep,
                                     history,
                                     state)
                substep_history.append(state)
    return results
