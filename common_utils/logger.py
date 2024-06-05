global Debug_Msg

Debug_Msg = True


def LogDebugMsgs(msg:str) -> None:
    """
        Log Debug Msgs that is used for debugging
        Inputs: msg: the debug msg to show
        output: N/A
    """
    if Debug_Msg:
        print(msg)