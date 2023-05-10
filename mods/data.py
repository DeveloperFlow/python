"""for primitive data manipulation"""
import re
def isNumeric(data):
    try: return type(int(data)) is int
    except Exception: 
        try: return type(float(data)) is float
        except Exception: return False