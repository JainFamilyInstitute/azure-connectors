import importlib
import itertools
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterator, Optional

from loguru import logger

EnvDict = dict[
    str, str
]  # type alias for a dictionary of environment variables and their values
EnvSet = set[str]  # type alias for a set of environment variables

# class AssignmentDict(TypedDict):
#     '''Dictionary of assignments of environment variables to env, envfile, or passed arguments.'''
#     env_vars: EnvDict
#     envfile_vars: EnvDict
#     passed_vars: EnvDict
#     omitted_vars: EnvDict
#     excluded_vars: EnvSet


def create_envfile_content(envfile_dict: EnvDict) -> str:
    '''Generate the content of a .env file from a dictionary. Each line is of the form "VAR=VALUE"'''
    return "\n".join([f"{var}={val}" for var, val in envfile_dict.items()]) + "\n"


def reload_all_modules() -> None:
    """Reload all modules in the 'src' directory"""
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
            logger.error(f"Error reloading module {module.__name__}: {e}")


def pack_dict_of_dicts(
    env_vars: EnvDict,
    envfile_vars: EnvDict,
    passed_vars: EnvDict,
) -> dict[str, EnvDict]:
    """Pack the dictionaries of environment variables into a dictionary of dictionaries."""

    packed = {
        "env_vars": env_vars,
        "envfile_vars": envfile_vars,
        "passed_vars": passed_vars,
    }

    return packed

def generate_assignments(dict_of_dicts: dict[str, EnvDict]) -> Iterator[dict[str,EnvDict]]:
    """
    Generate all possible combinations of assignments given a dictionary of possible variable assignments.

    Args:
        dict_of_dicts (dict[str, EnvDict]): A dictionary of dictionaries where the keys represent
            the assignment methods and the values represent the variables and their corresponding values.

    Yields:
        EnvDict: A dictionary of assignment methods and their corresponding variables and values.

    Example:
        >>> dict_of_dicts = {
        ...     "env_vars": {"VAR1": "value1", "VAR2": "value2"},
        ...     "envfile_vars": {"VAR2": "value2file", "VAR3": "value3file"},
        ...     "passed_vars": {"VAR3": "value3passed", "VAR4": "value4passed"},
        ... }
        >>> for combo in generate_combinations(dict_of_dicts):
        ...     print(combo)
        {'env_vars': {'VAR1': 'value1', 'VAR2': 'value2'}, 'envfile_vars': {'VAR3': 'value3file'}, 'passed_vars': {'VAR4': 'value4passed'}}
        {'env_vars': {'VAR1': 'value1', 'VAR2': 'value2'}, 'envfile_vars': {}, 'passed_vars': {'VAR3': 'value3passed', 'VAR4': 'value4passed'}}
        {'env_vars': {'VAR1': 'value1'}, 'envfile_vars': {'VAR2': 'value2file', 'VAR3': 'value3file'}, 'passed_vars': {'VAR4': 'value4passed'}}
        {'env_vars': {'VAR1': 'value1'}, 'envfile_vars': {'VAR2': 'value2file'}, 'passed_vars': {'VAR3': 'value3passed', 'VAR4': 'value4passed'}}
    """
    # Create a dictionary of all variables, destructuring the inner dictionaries into a list of tuples
    # for example:
    # {
    #     "VAR1": [("env_vars", "value1")],
    #     "VAR2": [("env_vars", "value2"), ("envfile_vars", "value2file")],
    #     "VAR3": [("envfile_vars", "value3file")]
    # }

    possible_assignments = defaultdict(list)
    for assignment_method, method_dict in dict_of_dicts.items():
        for var_name, value in method_dict.items():
            possible_assignments[var_name].append((assignment_method, value))

    # Generate all combinations of methods for each variable
    # for example:
    # [
    #   [{'env_vars': {'VAR1': 'value1'}}],
    #   [{'env_vars': {'VAR2': 'value2'}}, {'envfile_vars': {'VAR2': 'value2file'}}],
    #   [{'envfile_vars': {'VAR3': 'value3file'}}]
    # ]

    combinations = [
        [
            {assignment_method: {var_name: value}}
            for assignment_method, value in method_values
        ]
        for var_name, method_values in possible_assignments.items()
    ]

    # Create the combined dicts
    for combination in itertools.product(*combinations):
        combined_dict: dict[str, EnvDict] = {assignment_method: {} for assignment_method in dict_of_dicts.keys()}
        for sub_dict in combination:
            for assignment_method, method_dict in sub_dict.items():
                combined_dict[assignment_method].update(method_dict)
        yield combined_dict

def generate_scenarios(
    *,
    env_vars: EnvDict,
    envfile_vars: EnvDict,
    passed_vars: Optional[EnvDict] = None,
    unrelated_vars: Optional[EnvDict] = None,
    excluded_vars: Optional[EnvSet] = None,
) -> Iterator[tuple[dict[str,EnvDict], EnvDict]]:
    """
    Generate scenarios for testing environment variable assignments.

    Args:
        env_vars (EnvDict): A dictionary of environment variables.
        envfile_vars (EnvDict): A dictionary of environment variables from an envfile.
        passed_vars (Optional[EnvDict]): A dictionary of variables to be passed as arguments. Defaults to None.
        unrelated_vars (Optional[EnvDict]): A dictionary of unrelated environment variables. Defaults to None.
        excluded_vars (Optional[EnvSet]): A set of excluded environment variables. Used in fixture. Defaults to None.

    Yields:
        tuple[AssignmentDict, EnvDict]: A pair of dictionaries representing an assignment for setup_env and the expected value test.

    """
    # yield a pair for each assignment: the first for passing to setup_env,
    # the second for the expected value test
    env_vars = dict(env_vars)
    envfile_vars = dict(envfile_vars)
    passed_vars = dict(passed_vars or dict())
    unrelated_vars = dict(unrelated_vars or dict())
    excluded_vars = set(excluded_vars or set())

    # if anything is in the omitted list and one of the dictionaries, complain
    omitted_overlap = excluded_vars & (
        env_vars.keys() | envfile_vars.keys() | passed_vars.keys()
    )

    if omitted_overlap:
        logger.warning(
            f"Excluded variables found in env_vars, envfile_vars, or passed_vars: {omitted_overlap}"
        )
    
    # add unrelated vars to both env_vars and envfile_vars
    if unrelated_vars:
        env_vars.update(unrelated_vars)
        envfile_vars.update(unrelated_vars)

    packed = pack_dict_of_dicts(env_vars, envfile_vars, passed_vars)

    for assignment in generate_assignments(packed):
        yield (
            assignment,
            {
                **assignment["env_vars"],
                **assignment["envfile_vars"],
                **assignment["passed_vars"],
            },
        ) 