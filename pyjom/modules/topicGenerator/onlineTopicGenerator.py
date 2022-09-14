from pyjom.commons import *
from pyjom.languagetoolbox import englishTopicModeling
import requests
# import jieba
from typing import Literal

def topicModeling(sentences: list[str], lang='en'): # specify language please?
    # python does not enforce type checking. use third party tool such as linter instead.
    if lang == 'en':
        topics = englishTopicModeling(sentences)
        return topics

def topicSelection(topics, selected_topic_set, mode:Literal['combined','separate']='combined'):
    import random
    mTopics = topics.copy()
    random.shuffle(mTopics)
    for topic in mTopics:
        words = topic[mode]
        words = [x for x in words if x not in selected_topic_set]
        if len(words) > 0:
            word = random.choice(words)
            selected_topic_set.add(word) # no need to go elsewhere.
            return word
    print("no topic this time")
    return None

def 

@decorator
def OnlineTopicGenerator(source='giphy',topic = [['samoyed','dog','cat'],['funny','cute']]):
    selected_topic_set = {topic} # common way to initialize a set.
    if source == 'giphy':
        waitForServerUp(8902, "nodejs giphy server")
        init=True
        keywords = topic
        while True:
            if random.random()> 0.5:
                mRandomPicture = requests.get("http://localhost:8902/random", params = {'q':keywords, 'rating':'g'}) # may you get stickers?
                mRandomPictureJson = mRandomPicture.json()
                randomPictureId = mRandomPictureJson['data'][0]['id']
            else:
                mSearchPicture = requests.get("http://localhost:8902/search", params={})
                mSearchPictureJson = mSearchPicture.json()
                randomPictureId = random.choice(mSearchPictureJson['data'])['id']

            mRelatedPictures = requests.get("http://localhost:8902/related", params = {'q':randomPictureId})
            mRelatedPicturesJson = mRelatedPictures.json()
            sentences = [x['title'] for x in mRelatedPicturesJson['data']]
            topics = topicModeling(sentences)
            selectedTopic = topicSelection(topics, selected_topic_set)
            keywords = " ".join([mTopic,selectedTopic]) # for next iteration.