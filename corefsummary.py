#import spacy
#import neuralcoref
from summarizer import Summarizer
from summarizer.coreference_handler import CoreferenceHandler
from stanfordcorenlp import StanfordCoreNLP
import nltk.data
import json



# takes the text summary and returns the noun phrase with the subject and the verb phrase with the subject
def get_noun_verb_phrases(summary):
    nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    sents = sent_tokenizer.tokenize(summary.strip())
    #print(sents)
    parsed_sents = []

    for i in range(len(sents)):
        parsed_sents.insert(i, (nlp.dependency_parse(sents[i])))

    # articles and demonstratives
    stop_words = ["a", "an", "the", "this", "that", "these", "those"]

    tokened_sents = []

    for i in range(len(parsed_sents)):
        tokened_sents.insert(i, nlp.word_tokenize(sents[i]))
        for e in parsed_sents[i]:
            if tokened_sents[i][e[2]-1] in stop_words:
                parsed_sents[i].remove(e)

    subject_indices = []
    #print(parsed_sents)

    for i in range(len(parsed_sents)):
        print(i)
        for e in parsed_sents[i]:
            if e[0] == 'nsubj' or e[0] == 'nsubjpass' or e[0] == 'csubj' or e[0] == 'root':
                print(e[0])
                #subject_indices.insert(i, [])
                subject_indices.append([])
                subject_indices[-1].insert(0, i)
                subject_indices[-1].insert(1, e[2])
                break


    for e in subject_indices:
        for w in parsed_sents[e[0]]:
            if w[1] in e[1:]:
                e.append(w[2])

    for e in subject_indices:
        for w in parsed_sents[e[0]]:
            if w[1] in e[1:]:
                if w[2] not in e[1:]:
                    e.append(w[2])

#    for i in range(len(parsed_sents)):
#        for e in parsed_sents[i]:
#            if e[1] in subject_indices[i]:
#                if e[2] not in subject_indices[i]:
#                    subject_indices[i].append(e[2])

    for s in subject_indices:
        s[1:] = sorted(s[1:])
        print(s)

    verb_phrase = []

    for e in subject_indices:
        verb_phrase.append([])
        for w in parsed_sents[e[0]]:
            if w[2] not in e[1:]:
                verb_phrase[-1].append(w[2])

    for s in verb_phrase:
        s.sort()

    np_vp = []
    symbols = [",", ".", "(", ")", "\"", ":", ";"]

    # stores noun/verb phrases into np_vp
    # every key concept has a list, 1st element is np, 2nd is vp
    for i in range(len(subject_indices)):
        np = ""
        vp = ""
        np_vp.append([])
        for ind in subject_indices[i][1:]:
            if tokened_sents[subject_indices[i][0]][ind-1] in symbols:
                np = np + tokened_sents[subject_indices[i][0]][ind-1]
            else:
                np = np + " " + tokened_sents[subject_indices[i][0]][ind-1]
        for ind in verb_phrase[i]:
            if tokened_sents[subject_indices[i][0]][ind-1] in symbols:
                vp = vp + tokened_sents[subject_indices[i][0]][ind-1]
            else:
                vp = vp + " " + tokened_sents[subject_indices[i][0]][ind-1]
        np_vp[i].insert(0, np)
        np_vp[i].insert(1, vp)

    nlp.close()

    return np_vp


#nlp = spacy.load('en_core_web_lg')
#neuralcoref.add_to_pipe(nlp, greedyness=0.5)

with open("section4.txt", 'r') as myfile:
    text = myfile.read()
#text = text.replace("\n", " ")

#doc = nlp(text)

#if doc._.has_coref:
#print("corefs found")

#resolved_doc = doc._.coref_resolved
lines = text.split("\n")
#print(lines)

subsectionCount = -1
subsectionTitle = []
subsectionText = []
first_line = ""

#print("range of lines is ", len(lines))

for i in range(len(lines)):
    if i == 0:
        #print("first value hits")
        first_line = lines[0]
    elif lines[i].isupper():
        subsectionCount+= 1
        subsectionTitle.insert(subsectionCount, lines[i])
        subsectionText.insert(subsectionCount, "")
    elif lines[i] == "":
        continue
    else:
        subsectionText[subsectionCount]+= " " + lines[i]

#print(first_line)
#print(subsectionTitle[0])
#print(subsectionText[0])
handler = CoreferenceHandler(greedyness=0.5)
subsectionSummaries = []
model = Summarizer(sentence_handler=handler)
#result = model(subsectionText[1])

phrases = []

for i in range(len(subsectionText)):
    subsectionSummaries.insert(i, model(subsectionText[i], ratio=0.3, min_length=50))
    #print(subsectionSummaries[i])
    phrases.insert(i, get_noun_verb_phrases(subsectionSummaries[i]))


final = {
    'name': first_line,
    'children' : []
}


subject_list = []
repeat = False
index = 0

for i in range(len(phrases)):
    final['children'].insert(i, {'name': subsectionTitle[i], 'children' : []})
    for n in range(len(phrases[i])):
        for t in range(len(subject_list)):
            if phrases[i][n][0].lower() == subject_list[t][0].lower():
                repeat = True
                index = t
                break
        if (repeat == True):
            subject_list[index].append(phrases[i][n][1])
            repeat = False
        else:
            subject_list.append(phrases[i][n])

    concept_info = []
#final['children'][i]['children'] = subject_list
    for k in range(len(subject_list)):
        concept_info.insert(k, {'name': subject_list[k][0], 'children': []})
        for j in subject_list[k][1:]:
            concept_info[k]['children'].append({'name': j})
#final['children'][i]['children'].insert(k, {'name': subject_list[k][0]}, 'children': [])
#final['children'][i]['children'].insert(n, {'children': subject_list[1:]})
    final['children'][i]['children'] = concept_info

    subject_list = []


with open("section4JSON.json", "w") as wf:
    json.dump(final, wf, indent = 2)



#print(subsectionSummaries)


#print("\n\n", subsectionSummaries[1])
#document = ''.join(result)
#summaryText = open("sec4summaryMaxDist.txt", 'w')

#summaryText.write(first_line)
#summaryText.write("\n")

#for i in range(len(subsectionSummaries)):
#    summaryText.write(subsectionTitle[i])
#    summaryText.write("\n")
#    summaryText.write(subsectionSummaries[i])
#    summaryText.write("\n")

#summaryText.close

