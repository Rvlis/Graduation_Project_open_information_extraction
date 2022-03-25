def open_csv(name, pmode="w"):
    """
    创建csv文件
    :param pmode: ["w", "a"]
    """
    return csv.writer(open("../data/{}.csv".format(name), mode=pmode, newline="",encoding="utf-8"), doublequote=False, escapechar="\\")

