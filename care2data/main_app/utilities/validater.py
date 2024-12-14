def validate_name(name:str) -> bool:
    
    if len(name) < 4 or len(name) > 20:return False
    if len(name.replace(" ","")) < 4:return False
    return True
        
def name_corrector(name:str) -> str:
    name = name.split(" ")
    new_name = ""
    for i in name:
        if i != "":
            new_name += i+" "
    new_name=new_name.removesuffix(" ")
    return new_name
