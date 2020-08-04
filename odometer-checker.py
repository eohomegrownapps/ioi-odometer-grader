import checkerlib
from dmoj.result import CheckerResult


def check(process_output, judge_output, **kwargs):
    subtask = kwargs["batch"]
    grid = kwargs["judge_input"].decode("utf-8")
    subtask_id = f"[SUBTASK {subtask}]"
    process_output = process_output.decode("utf-8")
    try:
        ind = process_output.find(subtask_id) + len(subtask_id)
        endind = process_output[ind:].find("[SUBTASK")
        if endind == -1:
            endind = len(process_output)
        program = process_output[ind : ind + endind]
        if subtask == 1:
            result = checkerlib.checkSubtask1(grid, program, use_compile=False)
        elif subtask == 2:
            result = checkerlib.checkSubtask2(grid, program, use_compile=False)
        elif subtask == 3:
            result = checkerlib.checkSubtask3(grid, program, use_compile=True)
        elif subtask == 4:
            result = checkerlib.checkSubtask4(grid, program, use_compile=True)
        elif subtask == 5:
            result = checkerlib.checkSubtask5(grid, program, use_compile=True)
    except Exception:
        result = (False, "Error while parsing or running program")
    if result[0] is False:
        return CheckerResult(False, 0, result[1])
    elif result[1] == 1:
        return True
    else:
        return CheckerResult(
            True, result[1] * kwargs["point_value"], "Partially correct"
        )
