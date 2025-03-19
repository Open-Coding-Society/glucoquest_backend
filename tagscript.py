import talk
import random as r

class tag:
    def __init__(self,tags,total):
        self.tags = {"all":1}
        self.total = 1

    def newTag(self,lst):
        for tag in lst:
            if tag in self.tags:
                self.tags[tag] += 1
            else:
                self.tags[tag] = 1

    def recommend(self):
        # possibleItems = []
        t = sum(self.tags.values())
        normalized_weights = {k: v / t for k, v in self.tags.items()}

        keys = list(self.tags.keys())
        weights = [normalized_weights[k] for k in keys]
        biased_weights = [w**2 for w in weights]
        biased_total = sum(biased_weights)
        final_weights = [w / biased_total for w in biased_weights]
        r.choices(keys, weights=final_weights, k=1)[0]

def searchToTag(string):
    lst = string.split("split")
    for tag in lst:
        tag.newTag(tag)

ftalk = talk.Data()
print(ftalk)