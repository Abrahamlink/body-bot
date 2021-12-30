def my_iterator(data):
    values = list()
    for item in data:
        thing = item.copy()
        for el in thing:
            if type(el) == tuple:
                for i in el:
                    thing.insert(thing.index(el), i)
                thing.remove(el)
        values.append(thing)
    return values
