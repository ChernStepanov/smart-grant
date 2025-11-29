import json
import os


def saveSC(name, sc):
    with open(f"SmartContracts/{name}.json", "w", encoding="utf-8") as f:
            json.dump(sc, f, ensure_ascii=False, indent=2)

def readSC(name):
      with open(f"SmartContracts/{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
      
def getSCs():
    folder = r"SmartContracts"
    return [name[:-5] for name in os.listdir(folder)]
        