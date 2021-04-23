# Mind-Mapping

This project was done for the MTSU Honors College Thesis program. The goal of this is to create an automated mind mapping system in which the input of the system is a section from a history textbook and the output is a mind map inspired graph.


Libraries/input used:
- NeuralCoref (https://github.com/huggingface/neuralcoref)
- Stanford Core NLP (https://github.com/Lynten/stanford-corenlp)
- BERT Summarizer (https://github.com/dmmiller612/bert-extractive-summarizer)
- pdfPlumber (https://github.com/jsvine/pdfplumber)
- U.S. History by OpenStax (https://openstax.org/details/books/us-history)

How To Use:
- download the pdf from https://openstax.org/details/books/us-history
- run pdfToText.py with U.S._History.pdf as the input to get textbook.txt
- pick sections from textbook.txt to be analyzed
- run corefsummary.py with desired section (Must be running the Stanford CoreNLP server)

```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```
*In order to run the server, CoreNLP must be downloaded (https://stanfordnlp.github.io/CoreNLP/download.html)

- the resulting JSON file then needs to be passed to the d3test.html where it can be rendered in a web browser
