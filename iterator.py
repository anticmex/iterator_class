import json
import wikipediaapi
from tqdm import tqdm
import hashlib


class WikiUrlIter:

    def __init__(self, json_file, end=0):
        self.json_file = json_file
        self.start = 0
        self.end = end
        self.wiki_wiki = wikipediaapi.Wikipedia('en')

        with open(self.json_file, "r") as rf:
            self.file_data = json.load(rf)

        if self.end == 0:
            self.common_count = len(self.file_data) - 1
        else:

            self.common_count = self.end

        self.country_name = self.wiki_wiki.page(self.file_data[self.start]['name']['common'])
        self.country_url = self.country_name.fullurl

        self.local_dict = {self.country_name: self.country_url}

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start > self.common_count:
            raise StopIteration
        self.country_name = self.wiki_wiki.page(self.file_data[self.start]['name']['common'])
        self.country_url = self.country_name.fullurl
        self.local_dict = {self.country_name: self.country_url}

        return self.local_dict

    def __len__(self):
        return self.common_count


NewClass = WikiUrlIter("countries.json", 4)

for i in tqdm(NewClass, total=NewClass.__len__()):
    with open("url_link.txt", "a", encoding='utf-8') as f:
        f.write(str(i) + "\n")


def md5_encoder(iterator_class):
    start = 0
    end = iterator_class.__len__()

    while start < end:
        iter_link = iterator_class.country_url
        yield hashlib.md5(str(iter_link).encode()).hexdigest()
        start += 1


for item in md5_encoder(NewClass):
    print(item)
