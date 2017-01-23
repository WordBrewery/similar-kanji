#!/usr/bin/env python3

import json
from file.similars_file import SimilarsFile

class LookalikeBlender(object):

    def __init__(self, original='kanji.tgz_similars.ut8', similar='similar', output='kanji.tgz_similars.ut8'):
        self.original = SimilarsFile(original)
        self.similar = json.load(open(similar))
        self.output = SimilarsFile(output, self.original.kanji)
        try:
            with open('not_similar') as f:
                self.not_similar = json.load(f)
        except:
            self.not_similar = dict()

    def start(self):
        i = None
        for k in self.similar:
            if i == 'a':
                break
            for lookalike in self.similar[k]['similar']:
                if lookalike == k or lookalike in self.output.get_similar(k) or k in (self.not_similar.get(lookalike) or []):
                    continue
                i = input('Do {} and {} look similar? (Y(es)/n(o)/a(bort)):'.format(k, lookalike))
                if i == 'a':
                    break
                if i == 'n':
                    if not self.not_similar.get(k):
                        self.not_similar[k] = [lookalike]
                    elif not lookalike in self.not_similar[k]:
                        self.not_similar[k].append(lookalike)
                    if not self.not_similar.get(lookalike):
                        self.not_similar[lookalike] = [k]
                    elif not k in self.not_similar[lookalike]:
                        self.not_similar[lookalike].append(k)
                else:
                    self.output.set_similar(k, lookalike)
        self.output.write()
        with open('not_similar', 'w') as f:
            json.dump(self.not_similar, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    blender = LookalikeBlender()
    blender.start()
