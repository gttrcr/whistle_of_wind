import importlib
import argparse
import traceback
import utils
import os
from BasicView import BasicView


def start_a_module(module):
    class_name = "View"
    module = f"{module}.{class_name}"

    try:
        dynamic_module = importlib.import_module(module)
        try:
            dynamic_function = getattr(dynamic_module, class_name)
            if hasattr(dynamic_function, "view"):
                try:
                    dynamic_function().view()
                except Exception as e:
                    BasicView.basic_view_show_message(
                        "WOW",
                        f"Error during the execution of {module}:\n{traceback.format_exc()}",
                        3,
                    )
            else:
                BasicView.basic_view_show_message(
                    "WOW",
                    f"Cannot load method view() in class {class_name} from module {module}:\n{traceback.format_exc()}",
                    3,
                )
        except:
            BasicView.basic_view_show_message(
                "WOW",
                f"Cannot load class {class_name} from module {module}:\n{traceback.format_exc()}",
                3,
            )
    except:
        BasicView.basic_view_show_message(
            "WOW", f"Cannot load module {module}:\n{traceback.format_exc()}", 3
        )


parser = argparse.ArgumentParser(description="wow command line")
parser.add_argument(
    "tool", type=str, nargs="?", help="The name of the tool you want to use."
)
args = parser.parse_args()
if args.tool:
    tool = args.tool
else:
    modules = dict(
        map(
            lambda x: (utils.module_to_name(x), x),
            list(
                filter(
                    lambda x: not x.startswith("__"), utils.list_folders(os.getcwd())
                )
            ),
        )
    )

    tool, index = BasicView.basic_view_checkbox_list(
        "WOW", "Select a tool", modules.keys(), True
    )

if tool:
    start_a_module(modules[tool])
