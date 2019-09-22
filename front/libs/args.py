def check_empty_args(args):
    """
    检查空参数
    :param args: 
    :return:
    """
    for key in args:
        if args[key] == "":
            raise KeyError(key)
    # elif type(args) is str:
    #     if args == "":
    #         raise KeyError(get_variable_name(args))


# def get_variable_name(x):
#     for k,v in locals().items():
#         if v is x:
#             return k
