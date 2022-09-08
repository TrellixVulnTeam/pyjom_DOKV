# example of TDD.
import os

os.environ['http_proxy'] = ""
os.environ['https_proxy'] = ""
os.environ['all_proxy'] = ""

tests = [
    ["リンの麺は終わった", "リンの麺は終わった"],
    # only japanese
    [
        "リンの麺は終わった Lina的面吃完了没有",
        "リンの麺は終わった Lina的面吃完了没有",
    ],  # japanese with chinese containing english
    [
        "Lina I miss you Lina我想你了",
        "Lina I miss you Lina我想你了",
    ],  # english with chinese containing english
    ["向前冲 冲 冲", "向前冲 冲 冲"],  # only chinese
    ["go go go", "go go go"],  # chinese containing english (overall)
]
# build a classifier for this? wtf?

# whatlang?


def lastSpaceSpliter(text):
    text = text.strip()
    # index = 0
    for index in range(len(text)-1,-1, -1):
        # print(index)
        elem = text[index]
        if elem == " ":
            print("LAST SPACE FOUND AT %d", index)
            # do it right now, and return the value here.
            mTuple = (text[0:index], text[index:])
            return mTuple, True
    return text, False  # not a list.


# if there is a single shit failed to pass this 'lastSpaceSpliter' test, this is not a bilingual lrc file from netease.


for test in tests:
    print("_______________TEST SUBJECT_______________")
    for elem in test:
        print(elem)
    print("_______________TEST SUBJECT_______________")
    flags = [int(flag) for _, flag in [lastSpaceSpliter(elem) for elem in test]]
    print(flags)
    if sum(flags) < len(flags)*0.8:
        print("NOT A BILIGUAL LYRICS FILE")
    else:
        # having the potential of being a bilingual shit.
        # process this shit separately.
        # double check if this is really bilingual.
        foreignLangList = []
        nativeLangList = []
        for elem in test:
            text, flag = lastSpaceSpliter(elem)
            if flag:
                # this line might be bilingual.
                foreignLang, nativeLang = text
                foreignLangList.append(foreignLang)
                nativeLangList.append(nativeLang)
        nativeLangFlagStandard = "Cmn"
        foreignLangString = " ".join(foreignLangList)
        nativeLangString = " ".join(nativeLangList)

        # import whatlang
        # foreignLangFlag = whatlang.detect_language(foreignLangString)
        # nativeLangFlag = whatlang.detect_language(nativeLangString)
        
        # import cld3
        # nativeLangFlagStandard = "zh"
        # foreignLangFlag = cld3.get_language(foreignLangString)
        # nativeLangFlag = cld3.get_language(nativeLangString)

        from textblob import TextBlob

        foreignLangFlag = TextBlob(foreignLangString).detect_language()
        nativeLangFlag = TextBlob(nativeLangString).detect_language()
        print(foreignLangFlag)
        print(nativeLangFlag)
        # breakpoint()
        if foreignLangFlag[0] != nativeLangFlagStandard and nativeLangFlag[0] == nativeLangFlagStandard:
            # this is for sure the bilingual shit.
            print("BILINGUAL LYRIC FILE IDENTIFIED.")
        else:
            print("NOT A BILIGUAL LYRICS FILE")