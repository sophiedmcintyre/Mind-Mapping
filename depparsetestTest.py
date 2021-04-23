# Simple usage
from stanfordcorenlp import StanfordCoreNLP
import nltk.data

nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

text = 'Popular culture in the first half of the nineteenth century reflected the aversion to Indians that was pervasive during the Age of Jackson. Jackson skillfully played upon this racial hatred to engage the United States in a policy of ethnic cleansing, eradicating the Indian presence from the land to make way for white civilization. George Catlin produced many paintings of native peoples, which George Catlin offered as true representations despite routinely emphasizing their supposed savage nature. Accuracy aside, the painting captured the imaginations of white viewers, reinforcing their disgust at the savagery of Indians.'

sents = sent_tokenizer.tokenize(text.strip())
#print(nlp.word_tokenize(sentence))
#print "Part of Speech:", nlp.pos_tag(sentence)
#print 'Named Entities:', nlp.ner(sentence)
#print(nlp.parse(sentence))
parsed_sents = []

for i in range(len(sents)):
    parsed_sents.insert(i, (nlp.dependency_parse(sents[i])))
#print(nlp.parse(sent))
#print(nlp.coref(sentence))
#print(parsed_sents)

# articles and demonstratives
stop_words = ["a", "an", "the", "this", "that", "these", "those"]

tokened_sents = []

for i in range(len(parsed_sents)):
    tokened_sents.insert(i, nlp.word_tokenize(sents[i]))
    for e in parsed_sents[i]:
        if tokened_sents[i][e[2]-1] in stop_words:
            parsed_sents[i].remove(e)

#print(parsed_sents)
subject_indices = []

for i in range(len(parsed_sents)):
    for e in parsed_sents[i]:
        if e[0] == 'nsubj':
            subject_indices.insert(i, [])
            subject_indices[i].append(e[2])
            break

for i in range(len(parsed_sents)):
    for e in parsed_sents[i]:
        if e[1] in subject_indices[i]:
            subject_indices[i].append(e[2])

#print(subject_indices)

for i in range(len(parsed_sents)):
    for e in parsed_sents[i]:
        if e[1] in subject_indices[i]:
            if e[2] not in subject_indices[i]:
                subject_indices[i].append(e[2])

#print("NP: ", subject_indices)


for s in subject_indices:
    s.sort()

verb_phrase = []

for i in range(len(parsed_sents)):
    verb_phrase.insert(i, [])
    for e in parsed_sents[i]:
        if e[2] not in subject_indices[i]:
            verb_phrase[i].append(e[2])

#print("VP: ", verb_phrase)


#organize list and print out noun phrases (also figure out how to handle two subjects) check if subjects are same?

for s in verb_phrase:
    s.sort()

#print("NP: ", subject_indices)
#print("VP: ", verb_phrase)

for i in range(len(tokened_sents)):
    np = ""
    vp = ""
    for ind in subject_indices[i]:
        np = np + " " + tokened_sents[i][ind-1]
    for ind in verb_phrase[i]:
        vp = vp + " " + tokened_sents[i][ind-1]

    print("NP: ", np)
    print("VP: ", vp)

nlp.close()



