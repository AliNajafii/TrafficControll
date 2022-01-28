
def decode_value(value):
        if value != None:
            if isinstance(value,(list,tuple,set)):
                return [v.decode() for v in value if isinstance(value,bytes)]

            elif isinstance(value,dict):
                temp = {}
                for k,v in value.items() :

                    if isinstance(k,bytes) :
                        if isinstance(v,bytes):
                            temp[k.decode()] = v.decode()
                            continue
                        temp[k.decode()] = v
                    else :
                        if isinstance(v,bytes):
                            temp[k] = v.decode()
                            continue
                        temp[k] = v

                return temp

            elif isinstance(value,bytes):
                return value.decode()
            
            return value