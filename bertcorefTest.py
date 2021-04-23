from summarizer import Summarizer
from summarizer.coreference_handler import CoreferenceHandler

handler = CoreferenceHandler(greedyness=0.4)
# How coreference works:
# >>>handler.process('''My sister has a dog. She loves him.''', min_length=2)
# ['My sister has a dog.', 'My sister loves a dog.']

with open("sec2testing.txt", 'r') as myfile:
    body = myfile.read()

body = body.replace("\n", " ")

model = Summarizer(sentence_handler=handler)
doc = model(body, ratio=0.4, min_length=50)
print(doc)
