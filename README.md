# NLU-flight-ticket

This program is part of [a larger project](https://github.com/weidadeqiangge/CSCI544_Group33/) that aims to build a dialogue system that can interact with the user via voice, and help the user to book a flight ticket. This part of the project aims to build the language understanding module that can extract formatted information from text input.

There are 3 files in this program:
* `understand.py` is a rule-based implementation of the expected language understanding functionality;
* `understand_crf.py` is a machine learning based implementation, which contains all the training, predicting, testing and information extraction code;
* `gen_utterances.py` is a tool to generate training and testing data for the use of this project.

You can see my [project report](https://github.com/Shane-Xie-He/NLU-flight-ticket/raw/master/Report.pdf) for detailed explanation of my implementation.
