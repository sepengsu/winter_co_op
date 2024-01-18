def printing_var(obj):
    var = dict()
    for attr in dir(obj):
        if not attr.startswith("__"):
            try: 
                getattr(obj, attr)()
            except:
                print(f"{obj} = {getattr(obj, attr)}")
                var[obj] = getattr(obj,attr)
            else:
                print(f"{attr} = {getattr(obj, attr)()}")
                var[obj] = getattr(obj,attr)()
    
def direxcept(obj):
    oblist = dir(obj)
    return [attr for attr in oblist if not attr.startswith('_')]

def namedict(obj):
    return {item.name():item for item in obj}