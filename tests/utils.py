import importlib
import itertools
import sys
from pathlib import Path
from loguru import logger
from typing import Optional, Iterator

EnvDict = dict[str, str] # type alias for a dictionary of environment variables and their values
AssignmentDict = dict[str, EnvDict] # type alias for a dictionary of assignments of enviroment variables to env or envfile
EnvSet = set[str] # type alias for a set of environment variables


def create_envfile_content(envfile_dict: EnvDict) -> str:
    # Generate the content of a .env file from a dictionary
    return "\n".join([f"{var}={val}" for var, val in envfile_dict.items()]) + "\n"


def reload_all_modules() -> None:
    # This function reloads all modules in the 'src' directory
    # A little brute-force, but handles problems with module caching causing
    # the env_file.ENV_FILE variable not to propagate to the pydantic_settings classes
    # between tests

    src_path = Path(__file__).resolve().parent.parent / "src"
    for module in list(sys.modules.values()):
        try:
            if (
                module
                and hasattr(module, "__file__")
                and str(module.__file__).startswith(str(src_path))
            ):
                importlib.reload(module)
        except Exception as e:
            print(f"Error reloading module {module.__name__}: {e}")


def filter_by_assignment(
    vars: EnvDict, assignment: tuple[str, ...], target: str
) -> EnvDict:
    if not len(vars) == len(assignment):
        raise ValueError("Length of vars and assignment must be the same")

    return {
        k: v
        for (k, v), assign_to in zip(vars.items(), assignment)
        if assign_to == target
    }


def generate_assignment_dicts(
    env_vars: EnvDict,
    envfile_vars: EnvDict,
    unrelated_vars: EnvDict,
    excluded_vars: Optional[EnvSet] = None,
) -> Iterator[AssignmentDict]:
    # Yield all possible assignments of overlap variables and unrelated variables to env or envfile
    # Where:
    # - variables only in env_dict are assigned to "env"
    # - variables only in envfile_dict are assigned to "envfile"
    # - variables in both are assigned in every combination to exactly one of them
    # - unrelated variables can be assigned to "env", "envfile", or None
    # producing a list of dictionaries, each containing the assignments for each variable

    overlap_keys = env_vars.keys() & envfile_vars.keys()

    # get the overlap variables
    overlap_env_vars = {k: v for k, v in env_vars.items() if k in overlap_keys}
    overlap_envfile_vars = {k: v for k, v in envfile_vars.items() if k in overlap_keys}
    
    # filter out overlap variables to get solo_env_vars and solo_envfile_vars
    solo_env_vars = {k: v for k, v in env_vars.items() if k not in overlap_keys}
    solo_envfile_vars = {k: v for k, v in envfile_vars.items() if k not in overlap_keys}


    # produce every combination of assignments for overlap variables to env or envfile
    # -- gives an iterator of tuples of the form ('env', 'env', 'envfile', ...)
    overlap_assignments = itertools.product(
        ["env", "envfile"], repeat=len(overlap_keys)
    )
    
    # same for unrelated variables -- to env, envfile, or omitted
    unrelated_assignments = itertools.product(
        ["env", "envfile", "omitted"], repeat=len(unrelated_vars)
    )
    
    # now generate every possible combination of these two iterators
    combined_assignments = itertools.product(overlap_assignments, unrelated_assignments)

    # and spit out the corresponding AssignmentDict for each combination
    yield from (
        {
            "env_vars": {
                **solo_env_vars,
                **filter_by_assignment(overlap_env_vars, overlap_assignment, "env"),
                **filter_by_assignment(unrelated_vars, unrelated_assignment, "env"),
            },
            "envfile_vars": {
                **solo_envfile_vars,
                **filter_by_assignment(overlap_envfile_vars, overlap_assignment, "envfile"),
                **filter_by_assignment(unrelated_vars, unrelated_assignment, "envfile"),
            },
            "omitted_vars": filter_by_assignment(unrelated_vars, unrelated_assignment, "omitted"),
            "excluded_vars": excluded_vars,
        }
        for overlap_assignment, unrelated_assignment in combined_assignments
    )


def generate_scenarios(
    env_vars: EnvDict,
    envfile_vars: EnvDict,
    unrelated_vars: EnvDict,
    excluded_vars: Optional[EnvSet] = None,
) -> Iterator[tuple[AssignmentDict, EnvDict]]:
    # yield a pair for each assignment: the first for passing to setup_env,
    # the second for the expected value test
    if excluded_vars is None:
        excluded_vars = set()

    # if anything is in the omitted list and one of the dictionaries, complain
    omitted_overlap = excluded_vars & (env_vars.keys() | envfile_vars.keys())
    if omitted_overlap:
        logger.warning(
            f"Excluded variables found in env_dict or envfile_dict: {omitted_overlap}"
        )

    for assignment in generate_assignment_dicts(
        env_vars, envfile_vars, unrelated_vars, excluded_vars
    ):
        yield (assignment, {**assignment["env_vars"], **assignment["envfile_vars"]})
