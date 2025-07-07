import argparse
import importlib
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Map of available steps to their corresponding module names
STEPS = {
    1: "step1_delete_empty_folders",
    2: "step2_delete_index_files",
    3: "step3_remove_desktop_ini",
    4: "step4_format_folders",
    5: "step5_create_C0_folders",
    6: "step6_organizate_files",
    7: "step7_subfolder_organization",
    8: "step8_create_electronic_index",
    9: "step9_check_folders",
    10: "step10_folders_repor",
    # Agrega más pasos aquí según tu proyecto
}


def run_step(step_number):
    try:
        module_name = STEPS[step_number]
        module = importlib.import_module(f"organizer.{module_name}")
        print(f"\n▶️ Running Step {step_number}: {module_name}")
        module.run()
        print(f"✅ Step {step_number} finished successfully.")
    except KeyError:
        print(f"❌ Step {step_number} is not defined.")
    except AttributeError:
        print(f"❌ 'run()' function not found in step {step_number}.")
    except Exception as e:
        print(f"❌ Error while executing step {step_number}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Run selected steps to organize your files."
    )
    parser.add_argument(
        "--steps",
        nargs="+",
        type=int,
        help="List of step numbers to run. Example: --steps 1 3",
    )
    args = parser.parse_args()

    if not args.steps:
        print(
            "⚠️  No steps specified. Use --steps followed by numbers.\n"
            "Example: --steps 1 2 3"
        )
        return

    for step in args.steps:
        run_step(step)


if __name__ == "__main__":
    main()
