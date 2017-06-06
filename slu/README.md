## SLU4P - Spoken Language Understanding 4 Pepper

This document provides a description of **SLU4P** - *Spoken Language
Understanding 4 Pepper*

*SLU4P* is composed of a complete collection of
modules that enable a fast design, development and deployment
of effective interactions through Natural Language with the Pepper robot.

It provides the following modules:
 
 *  **Speech-To-Text** -> ``speech_to_text``
 * **Speech Re-Ranking** -> ``speech_reranking``
 * **Language Understanding** -> ``language_understanding``
 * **Dialogue Management** -> ``dialogue_management``
 * **Text-To-Speech** -> ``test_to_speech``

###Requirements
 * `Python (2.7)`
 * `pynaoqi (> 2.5)`
 
###Installation

To use the modules, you need to set the library in the `PYTHONPATH`.

 * **Linux**
 
 ~~~
 echo 'export PYTHONPATH=${PYTHONPATH}:/path/to/library' >> ~/.bashrc
 ~~~
 * **Mac**
 
 ~~~
 echo 'export PYTHONPATH=${PYTHONPATH}:/path/to/library' >> ~/.bash_profile
 ~~~

###Speech-To-Text

 * **Resources**
    * *Nuance grammar*: 
    * *GoogleAPI keys*: 

~~~
usage: speech_recognition.py [-h] [-i PIP] [-p PPORT] [-l LANG]
                             [--word-spotting] [--no-audio] [--no-visual]
                             [-v VOCABULARY] [-k KEYS]

optional arguments:
  -h, --help            show this help message and exit
  -i PIP, --pip PIP     Robot ip address
  -p PPORT, --pport PPORT
                        Robot port number
  -l LANG, --lang LANG  Use one of the supported languages (only English at
                        the moment)
  --word-spotting       Run in word spotting mode
  --no-audio            Turn off bip sound when recognition starts
  --no-visual           Turn off blinking eyes when recognition starts
  -v VOCABULARY, --vocabulary VOCABULARY
                        A txt file containing the list of sentences composing
                        the vocabulary
  -k KEYS, --keys KEYS  A txt file containing the list of the keys for the
                        Google ASR
~~~

#####TODO

 * Check the availability of the network connection (Google requirement): if not, deactivate Google ASR
 * Catch the requests limit error

###Speech Re-Ranking

 * **Resources**
    * *Domain-dependent noun dictionary*:
    * *Domain-dependent verb dictionary*:
    * *Nuance grammar*: 

 * **Dependencies**
    * `Speech Recognition`

~~~
usage: reranker.py [-h] [-i PIP] [-p PPORT] [-a ALPHA] [-n NOUN_COST]
                   [-v VERB_COST] [-g GRAMMAR_COST] [-u NUANCE_COST]
                   [--noun-dictionary NOUN_DICTIONARY]
                   [--verb-dictionary VERB_DICTIONARY]
                   [--nuance-grammar NUANCE_GRAMMAR]

optional arguments:
  -h, --help            show this help message and exit
  -i PIP, --pip PIP     Robot ip address
  -p PPORT, --pport PPORT
                        Robot port number
  -a ALPHA, --alpha ALPHA
                        Alpha parameter for the additive smoothing of the
                        prior distribution
  -n NOUN_COST, --noun-cost NOUN_COST
                        Cost for the noun posterior distribution
  -v VERB_COST, --verb-cost VERB_COST
                        Cost for the verb posterior distribution
  -g GRAMMAR_COST, --grammar-cost GRAMMAR_COST
                        Cost for the grammar posterior distribution
  -u NUANCE_COST, --nuance-cost NUANCE_COST
                        Cost for the Nuance posterior distribution
  --noun-dictionary NOUN_DICTIONARY
                        A txt file containing the list of domain nouns
  --verb-dictionary VERB_DICTIONARY
                        A txt file containing the list of domain verbs
  --nuance-grammar NUANCE_GRAMMAR
                        A txt file containing the list of sentences composing
                        the vocabulary
~~~

###Language Understanding

 * **Resources**

 * **Dependencies**
    * `Speech Recognition`

###Dialogue Management

 * **Resources**

 * **Dependencies**
    * `Speech Recognition`

~~~
usage: dialogue_manager.py [-h] [-i PIP] [-p PPORT] [-a AIML_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -i PIP, --pip PIP     Robot ip address
  -p PPORT, --pport PPORT
                        Robot port number
  -a AIML_PATH, --aiml-path AIML_PATH
                        Path to the root folder of AIML Knowledge Base
~~~

###Text-To-Speech

 * **Resources**

 * **Dependencies**
    * `Speech Recognition`
    * `Dialogue Management`

~~~
usage: text_to_speech.py [-h] [-i PIP] [-p PPORT]
                         [-l {contextual,random,disabled}]

optional arguments:
  -h, --help            show this help message and exit
  -i PIP, --pip PIP     Robot ip address
  -p PPORT, --pport PPORT
                        Robot port number
  -l {contextual,random,disabled}, --language-mode {contextual,random,disabled}
                        The body language modality while speaking
~~~

###References

###Acknowledgements