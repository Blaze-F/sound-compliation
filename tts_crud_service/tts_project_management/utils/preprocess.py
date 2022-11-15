import re


def preprocess_data(input):
    phase1 = input.strip()
    phase2 = re.compile(r"([^\.!?]*[\.!?])", re.M)
    phase3 = phase2.findall(phase1)
    result = [re.sub("[^\w|가-힣+?!.,\s]", "", i).strip() for i in phase3 if len(i) > 0]
    return result
