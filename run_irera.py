import os
os.environ["DSP_NOTEBOOK_CACHEDIR"] = os.path.join(".", "local_cache")

from dspy import Models
from src.data_loaders import load_data
from src.evaluators import create_evaluators
from src.programs import InferRetrieveRank

import argparse


def run_irera(state_path, dataset_name, do_validation, do_test):
    # load data (all of these files needed for the config could be dumped separately in one folder)
    (
        _,
        validation_examples,
        test_examples,
        _,
        _,
        _,
    ) = load_data(dataset_name)

    # load program
    program = InferRetrieveRank.load(state_path)

    # Validate / Test
    if do_validation:
        print("validating final program...")

        # # # ### loading 1 example for testing
        # validation_examples = validation_examples[:5]
        # print("example: ", validation_examples)
        validation_evaluators = create_evaluators(validation_examples)
        validation_rp50 = validation_evaluators["rp50"](program)
        validation_rp10 = validation_evaluators["rp10"](program)
        validation_rp5 = validation_evaluators["rp5"](program)
        print("Final program validation_rp50: ", validation_rp50)
        print("Final program validation_rp10: ", validation_rp10)
        print("Final program validation_rp5: ", validation_rp5)


    if do_test:
        print("testing final program...")
        test_evaluators = create_evaluators(test_examples)
        test_rp10 = test_evaluators["rp10"](program)
        test_rp5 = test_evaluators["rp5"](program)

    if do_validation:
        print("Final program validation_rp50: ", validation_rp50)
        print("Final program validation_rp10: ", validation_rp10)
        print("Final program validation_rp5: ", validation_rp5)

    if do_test:
        print("Final program test_rp10: ", test_rp10)
        print("Final program test_rp5: ", test_rp5)

    return program


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Infer-Retrieve-Rank on an extreme multi-label classification (XMC) dataset."
    )

    # Add arguments
    parser.add_argument("--state_path", type=str)
    parser.add_argument("--lm_config_path", type=str)
    parser.add_argument(
        "--dataset_name",
        type=str,
        help="Specify the dataset",
    )
    parser.add_argument(
        "--do_validation",
        action="store_true",
        help="Specify if validation results need to be calculated (default: False)",
    )
    parser.add_argument(
        "--do_test",
        action="store_true",
        help="Specify if test results need to be calculated (default: False)",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    state_path = args.state_path
    lm_config_path = args.lm_config_path
    dataset_name = args.dataset_name
    do_validation = args.do_validation
    do_test = args.do_test

    print("state_path: ", state_path)
    print("lm_config_path: ", lm_config_path)
    print("dataset_name: ", dataset_name)
    print("do_validation: ", do_validation)
    print("do_test: ", do_test)


    Models(config_path=lm_config_path)

    program = run_irera(state_path, dataset_name, do_validation, do_test)
