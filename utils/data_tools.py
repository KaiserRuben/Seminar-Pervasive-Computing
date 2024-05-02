def flatten(l) -> list:
    """
    Flattens a list, no matter how nested it is
    :param l:
    :return: flat l
    """
    flat_list = []
    for elem in l:
        if type(elem) == list:
            flat_list.extend(flatten(elem))
        else:
            flat_list.append(elem)
    return flat_list