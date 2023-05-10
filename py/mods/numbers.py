"""module for number conversion to words and back"""
import data
import re

#the units conversion blue print
units = ["zero","one","two","three","four","five","six","seven","eight","nine"]

#the tens conversion blue print for tens from 10 - 19
tens1 = ["ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen",
"seventeen","eighteen","nineteen"]

#the tens conversion blue print for tens from 20 - 99
tens2 = ["twenty","thirty","fourty","fifty","sixty","seventy","eighty","ninety"]

#the rest of the conversion blue prints
others = {
    range(3,4):"hundred",
    range(4,7):"thousand",
    range(7,10):"million",
    range(10,13):"billion",
    range(13,16):"trillion"
}

def n2w(number):
    """converts numbers to words"""
    if not data.isNumeric(number): raise TypeError(f"number must be a number")
    strV = str(number); whole = strV; decimals = ""
    if "." in strV: 
        whole = strV[0:strV.index(".")]
        decimals = strV[strV.index(".") + 1:len(strV)]
    whole = int(whole)
    if whole < 0: minus = "minus "
    else: minus = ""
    whole = abs(whole)
    inWords = n2wProcess(whole)
    for i,decimal in enumerate(decimals):
        decimalInWord = units[int(decimal)]
        point = ""
        if i == 0: point = " point"
        inWords = f"{inWords}{point} {decimalInWord}"
    return f"{minus}{inWords}"

def n2wProcess(number):
    strV = str(number)
    numLen = len(strV)
    
    #if it is still in units
    if numLen == 1:
        return units[number]
    #if it is in the range of 10 - 19
    if number in range(10,20):
        return tens1[number - 10]
    #if it is in the range of 20 - 99
    if number in range(20,100):
        unitValue = number % 10
        inWords = number // 10
        inWords = tens2[inWords - 2]
        if unitValue > 0: unitValue = f" {n2wProcess(unitValue)}"
        else: unitValue = ""
        return f"{inWords}{unitValue}"
    #if it is in the range of 100 - scope of this code
    rangeStart = False
    for numRange in others:
        if numLen in numRange:
            inWords = others[numRange]
            rangeStart = numRange[0]
            pv = 10 ** (rangeStart - 1)
            break
    if not rangeStart: raise ValueError(f"number value out of conversion scope")
    sub = int(strV[0:numLen - rangeStart + 1])
    subInWord = n2wProcess(sub)
    inWords = f"{subInWord} {inWords}"
    rest = number - (sub * pv)
    if rest == 0: return inWords
    #check if there should be an "and"
    if pv >= 100 and rest < 100: inWords = f"{inWords} and"
    elif pv > rest and rest >= 100: inWords = f"{inWords},"
    return f"{inWords} {n2wProcess(rest)}"

def w2n(word):
    """conversion"""
    if not type(word) is str: raise(TypeError(f"{word} is not a string"))
    word = word.lower()
    word = word.replace(" and"," ")
    word = word.replace(","," ")
    word = word.strip()
    word = re.sub(" +"," ",word)
    word = word.split(" ")
    minus = ""; decimals = []
    if "minus" in word and word[0] == "minus": word.pop(0); minus = "-"
    if "point" in word: 
        decimals = word[word.index("point") + 1:len(word)] 
        word = word[0:word.index("point")]
    if "a" in word and word[0] == "a": word.pop(0)
    toNumber = w2nProcess(word)
    if len(decimals) > 0:
        toNumber = f"{toNumber}."
        for dn in decimals:
            if not dn in units:
                try: toNumber = f"{toNumber}{w2nProcess(decimals)}"; break
                except Exception: raise(ValueError(f"a magnitude couldn't be gotten for {dn}"))
            toNumber = f"{toNumber}{units.index(dn)}"
    toNumber = f"{minus}{toNumber}"
    try: toNumber = int(toNumber)
    except Exception: toNumber = float(toNumber)
    return toNumber
def w2nProcess(word):
    if len(word) == 0: return 0
    #first find the maximum number
    asNumber = []
    placeValues = []
    for aWord in word[0:5]:
        #first search in units
        if aWord in units:
            asNumber.append(units.index(aWord)); placeValues.append(1); continue
        #then check in tens1
        if aWord in tens1:
            asNumber.append(tens1.index(aWord) + 10); placeValues.append(10); continue
        #then check in tens2
        if aWord in tens2:
            asNumber.append((tens2.index(aWord) + 2) * 10); placeValues.append(10); continue
        #then check in others
        found = False
        for numRange in others:
            if others[numRange] == aWord: 
                pv = 10**(numRange[0] - 1)
                asNumber.append(pv); placeValues.append(pv)
                found = True; break
        if found: continue
        raise ValueError(f"The word \"{aWord}\" could not be converted to a number")
    maxPv = max(placeValues); maxIndex = placeValues.index(maxPv); maxNum = asNumber[maxIndex]
    thisSubject = word[0:maxIndex]; rest = word[maxIndex + 1:len(word)]
    if maxNum in range(0,20): return maxNum
    if maxPv == 10: return maxNum + w2nProcess(rest)
    sub = w2nProcess(thisSubject)
    if sub == 0: sub = 1
    return (sub * maxPv) + w2nProcess(rest)