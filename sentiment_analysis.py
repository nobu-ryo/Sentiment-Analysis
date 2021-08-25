
from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import tkinter as tk
import re

from Radarchart import plot_radarchart

#========================================== word2vec ===========================================

class EmotionAnalysis:
    def __init__(self, text):
        self.text = re.split('[\n|。|]', text)
        #self.text = text.split('。')
        #print(self.text)
        self.t = Tokenizer()
        self.model = None
        self.labels = ['喜び', '悲しみ', '怒り', '驚き', '恐れ', '嫌悪']
        self.labels2 = ['happiness', 'sadness', 'anger', 'surprise', 'fear', 'disgust'] #文字化けのため
        self.labelvalue = [0, 0, 0, 0, 0, 0]
        self.emphasis = ['とても','すごい','本当に']　#強調の単語

    def extract_words(self, s):
        tokens = self.t.tokenize(s)
        return [token.base_form for token in tokens if token.part_of_speech.split(',')[0] in ['名詞', '形容詞', '動詞', '副詞']]

    def make_new_model(self): #新しいモデルを作成
        with open(r"./textfolder/[your text file name]", encoding = "utf-8") as file:
            txt = file.read()
        sentences = txt.split('\n')
        word_list = [self.extract_words(sentence) for sentence in sentences]
        
        model = word2vec.Word2Vec(word_list, size = 100, min_count = 1, window = 5, iter = 100)
        model.save("[your favorite name].model")
        self.analysis()

    def load_model(self): #モデルのロード
        try:
            self.model = word2vec.Word2Vec.load("[your favorite name].model")
        except FileNotFoundError:
            print("モデルが見つかりません！New Modelボタンから実行してください。")

    def analysis(self): #分析
        self.load_model()
        word_list = [self.extract_words (sentence) for sentence in self.text]
        limit = 0 #類似度の下限
        i = 1 #強調
        for x in word_list:
            for y in x:
                if y in self.emphasis:
                    i = 2
                    continue
                token = self.t.tokenize(y).__next__().part_of_speech.split(',')[0]
                if (y in self.model.wv.vocab) and (y != "する") and (token != '副詞'):
                    for z in range(0, len(self.labels)):
                        if (i > 1) and (token == '形容詞' or token == '名詞'):
                            dos  = self.model.wv.similarity(self.labels[z], y) * i
                        else:
                            dos = self.model.wv.similarity(self.labels[z], y)
                        if dos > limit:
                            self.labelvalue[z] += dos
                i = 1
        print(self.labelvalue)
        a = 10
        for x in range(0, len(self.labelvalue)):
            if self.labelvalue[x] > a:
                a = self.labelvalue[x]


        for x in range(0, len(self.labelvalue)):
            if a > 10:
                self.labelvalue[x] = self.labelvalue[x] / (a / 10)
            self.labelvalue[x] = round(self.labelvalue[x])
        print(self.labelvalue)

        self.plot()
    
    def plot(self):
        plot_radarchart(self.labelvalue, self.labels2)

#=========================================== tkinter ===============================================
root = tk.Tk()
root.title("text")
root.geometry("400x170+100+100")
emotion = None

def analyze():
    result=text.get("1.0","end-1c")
    emotion = EmotionAnalysis(result)
    emotion.analysis()

def new_model_analyze():
    result = text.get("1.0", "end-1c")
    emotion = EmotionAnalysis(result)
    emotion.make_new_model()

text=tk.Text(root, height=10)
text.pack()
btnanalyze = tk.Button(root, height = 1, width = 5, text = "analyze", command = analyze)
btnanalyze.pack(padx = 30, side = tk.LEFT)
btnnewmodel = tk.Button(root, height = 1, width = 5, text = "New Model", command = new_model_analyze)
btnnewmodel.pack(padx = 25, side = tk.LEFT)
btnExit = tk.Button(root, height = 1, width = 5, text = "Exit", command = root.destroy)
btnExit.pack(padx = 30, side = tk.RIGHT)


root.mainloop()
