import json

def saveSC(name, json):
    with open(f"SmartContracts/{name}.json", "w", encoding="utf-8") as f:
            json.dump(json, f, ensure_ascii=False, indent=2)

def readSC(name):
      with open(f"SmartContracts/{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)