import nltk
from jellyfish import soundex
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


nltk.download('wordnet')


class VoiceProcess:
    lexer_sensitivity = 35

    def __init__(self, _command, tester_dict):
        self._command = _command
        self.tester_dict = tester_dict
        self.lemmatizer = WordNetLemmatizer()
        # self.tester_dict = {'check': [1, 2], 'test': [3, 4], 'play': [5, 6], 'click': [7, 8], 'fourth': [9, 10]}

    def dict_slicer(self, test_dict, first_letter, _command):
        return [i for i in test_dict.keys() if len(_command)==len(i) or (self._command in i or i in self._command)]

    def command_validator(self):
        percentages = []
        words = []
        if self._command in self.tester_dict:
            print("The command to be executed is:" + " " + self._command)
            return self._command
        elif self._command == "exit macro":
            return "exit macro"
        elif len(self.tester_dict) == 0:
            return "There is no such command"
        else:
            # input_choice = 0
            list_command_lemma = []
            list_command = list(self._command.split(" "))
            for i in list_command:
                _lemma = self.lemmatizer.lemmatize(i, pos=wordnet.VERB)
                # print("Lemma: ", _lemma)
                list_command_lemma.append(_lemma)
            _command_lemma = " ".join(list_command_lemma)
            for z in self.tester_dict.keys():
                if _command_lemma == z:
                    return z
                else:
                    for z in self.tester_dict:
                        if soundex(self._command) == soundex(z):
                            print("The command to be executed is:" + " " + z)
                            return z
                        else:
                            sliced_list = self.dict_slicer(self.tester_dict, self._command[0], self._command)
                            for i in sliced_list:
                                count_ = 0
                                if self._command in i:
                                    percentage = (len(self._command) / len(i)) * 100
                                    if 100 >= percentage >= (100 - VoiceProcess.lexer_sensitivity):
                                        percentages.append(percentage)
                                        words.append(i)
                                elif i in self._command:
                                    percentage = (len(i) / len(self._command)) * 100
                                    if 100 >= percentage >= (100 - VoiceProcess.lexer_sensitivity):
                                        percentages.append(percentage)
                                        words.append(i)
                                else:
                                    for j in range(len(self._command)):
                                        if i[j] == self._command[j]:
                                            count_ += 1
                                    percentage = (count_ / len(self._command)) * 100
                                    if 100 >= percentage >= (100 - VoiceProcess.lexer_sensitivity):
                                        percentages.append(percentage)
                                        words.append(i)
                            if len(percentages) != 0:
                                index_of_possible_command = np.argmax(percentages)
                                print("This", percentages)
                                print("The command to be executed is:" + " " + index_of_possible_command)
                                return index_of_possible_command



