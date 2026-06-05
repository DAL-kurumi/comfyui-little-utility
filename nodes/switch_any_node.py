"""
Switch (Any) - 依 select 索引從多個同類型輸入中選一個輸出
首個輸入連線後鎖定類型，並由前端動態新增 input2、input3...
"""

import inspect


class SwitchAnyNode:
    @classmethod
    def INPUT_TYPES(cls):
        optional = {
            "input1": ("*", {"lazy": True}),
        }
        stack = inspect.stack()
        if len(stack) > 2 and stack[2].function == "get_input_info":
            class _AnyInputs:
                def __contains__(self, item):
                    return True

                def __getitem__(self, key):
                    return "*", {"lazy": True}

            optional = _AnyInputs()

        return {
            "required": {
                "select": ("INT", {"default": 1, "min": 1, "max": 999999, "step": 1}),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("output",)
    FUNCTION = "switch_any"
    CATEGORY = "utils"

    def check_lazy_status(self, select, **kwargs):
        input_name = f"input{int(select)}"
        if input_name in kwargs:
            return [input_name]
        return []

    def switch_any(self, select, **kwargs):
        input_name = f"input{int(select)}"
        if input_name in kwargs:
            return (kwargs[input_name],)
        if "input1" in kwargs:
            return (kwargs["input1"],)
        return (None,)
