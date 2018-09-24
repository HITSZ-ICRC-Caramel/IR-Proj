import re
import os
import glob
import jieba
from process_data import get_boolean_model


class BooleanRetrieval:
    sign = set(['and', 'or', 'not', '(', ')'])
    instance = None
    table = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = BooleanRetrieval()
        return cls.instance


    def __init__(self):
        self.table = get_boolean_model()

    def check_tokens(self, tokens):
        status = 0
        for token in tokens:
            if token not in self.sign:
                status += 1
                if status > 1:
                    return False
        return True

    def search(self, query):
        query = query.strip()
        query = query.replace('(', '( ').replace(')', ' )')
        tokens = re.split(r'\s+', query)
        if not self.check_tokens(tokens):
            pass
        answer_list = []
        for doc_id, vector in self.table.items():
            to_eval = []
            for token in tokens:
                if token in self.sign:
                    to_eval.append(token)
                else:
                    to_eval.append(str(vector[token]))
            to_eval = ' '.join(to_eval)
            value = eval(to_eval)
            if value:
                answer_list.append(doc_id)
        return answer_list






