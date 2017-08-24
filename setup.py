from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import sys
import datetime
import nltk
from nltk import FreqDist
from pdfminer.pdfpage import PDFPage
import os
import shutil
from nltk.corpus import stopwords
from textblob.classifiers import NaiveBayesClassifier
import glob
import random

stop = stopwords.words('german')
#print(stop)
#print("\n\n\n\n")
# if there are no conflicting packages in the default Python Libs =>
sys.path.append("/usr/home/username/pdfminer");
def convert(fname, pages=None):
   # filename = fname;
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
        
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

file_list=glob.glob("InputFiles/*")
cnt=1
for filename in file_list:
    print(filename)
    strn=convert(filename)
    filename2=filename[11:]
    filetosave = strn;
    document = ' '.join([i for i in strn.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    xr=random.randint(0,999999)
    def check_special(x):
        if ';' in x:
            return False
        else:
            return True


    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    flattened = []
    for sublist in sentences:
        for val in sublist:
            flattened.append(val)

    myDict={}
    for word in flattened:
         if word in myDict:
              myDict[word]+=1
         else:
             myDict[word]=1
    new_flattened = []
    for key,value in myDict.items():
        new_flattened.append(key)
    new_words=[x for x in new_flattened if len(x)>2]
    new_words=[x for x in new_words if check_special(x)]


        
    ##new_words=[x for x in new_words if not '.' or not ':' in x]
    ##print(new_words)
    x=0
    H = [];
    S = [];
    V = [];
    total_length = len(new_words);
    #print ("new_words: ",new_words)
    hirish = open("TrainingData\\Hirsch.txt");
    SWB = open ("TrainingData\\swb.txt");
    vod = open ("TrainingData\\vodafone.txt");
    for line in hirish:
        line = line.split("\n")[0];
        H.append(line);
    for line in vod:
        line = line.split("\n")[0];
        V.append(line);

    #print(H)

    for line in SWB:
        line = line.split("\n")[0];
        S.append(line);

    #print(S)
    hirish_percentage = 0;
    swb_percentage = 0;
    vod_percentage = 0;
    for word in H:
        if word in new_words:
            hirish_percentage +=1;
    hirish_percentage = (hirish_percentage / len(H)) * 100;
    
    for word in V:
        if word in new_words:
            vod_percentage +=1;
    vod_percentage = (vod_percentage / len(H)) * 100;

    for word in S:
        if word in new_words:
            swb_percentage +=1;
    swb_percentage = (swb_percentage / len(S)) * 100;
    print("File processing number: "+str(cnt))
    cnt=cnt+1;
    print ("\nHirsch percentage: ",hirish_percentage);
    print ("SWB percentage: ",swb_percentage);
    print ("Vodafone percentage: ",vod_percentage);
    print ("\n")
    hirish.close();
    SWB.close();
    vod.close();
    s='Till'
    s1='Sara'
    name="none"
    if s in new_words:
        name=s;
        if s1 in new_words:
            name=s1+"-"+s
    elif s1 in new_words:
        name=s1;
    print(name)
    word1=""
    for word in new_words:
        try:
            datetime.datetime.strptime(word, '%d.%m.%Y');
            if("Oktober" in word):
                word = str.replace(word,"Oktober","10");
            word = word.split(".");
            start = word[0];
            word[0] = word[2];
            word[2] = start;
            word1 = word[0] + word[1] + word[2] 
            print (word1);
            break;
              
        except:
         try:
            datetime.datetime.strptime(word, '%d.%m.%y');
            if("Oktober" in word):
                word = str.replace(word,"Oktober","10");
            word = word.split(".");
            start = word[0];
            word[0] = word[2];
            word[2] = start;
            word1 = word[0] + word[1] + word[2] 
            print (word1);
            break;
              
         except:
            continue;
    
    if(hirish_percentage > swb_percentage and hirish_percentage > vod_percentage ):
     if(hirish_percentage < 70 and hirish_percentage >= 35):
         #filename1=str(word1)+" - Hirsch"+" - ("+name+
         
         #filename1 = str.replace(filename2,"tags_","C");
         newpath = 'ClassifiedOutputFiles\\Hirsch\\';
         if not os.path.exists(newpath):
            os.makedirs(newpath);
     
         #shutil.move(filename, newpath + "\\" + filename1);
         os.rename(filename,newpath+str(word1)+" - Hirsch"+" - ("+name+") "+"[c] _"+str(xr)+".pdf")
     elif (hirish_percentage < 35):
         newpath = 'ClassifiedOutputFiles\\Not_recognized\\';
         if not os.path.exists(newpath):
            os.makedirs(newpath);
     
         os.rename(filename,newpath+str(word1)+" - Hirsch"+" - ("+name+") _"+str(xr)+".pdf")
     else:
      newpath = 'ClassifiedOutputFiles\\Hirsch\\';
      if not os.path.exists(newpath):
          os.makedirs(newpath);
     
      os.rename(filename,newpath+str(word1)+" - Hirsch"+" - ("+name+") _"+str(xr)+".pdf")
      
    elif (swb_percentage > hirish_percentage and swb_percentage > vod_percentage):
        if(swb_percentage < 70 and swb_percentage >= 35):
          #filename1 = str.replace(filename2,"tags_","C");
          newpath = 'ClassifiedOutputFiles\\SWB\\';
          if not os.path.exists(newpath):
            os.makedirs(newpath);
     
          os.rename(filename,newpath+str(word1)+" - swb"+" - ("+name+") "+"[c] _"+str(xr)+".pdf")
        elif (swb_percentage < 35):
           newpath = 'ClassifiedOutputFiles\\Not_recognized\\';
           if not os.path.exists(newpath):
              os.makedirs(newpath);

           os.rename(filename,newpath+str(word1)+" - swb"+" - ("+name+") _"+str(xr)+".pdf")
        else:
         newpath = 'ClassifiedOutputFiles\\SWB\\';
         if not os.path.exists(newpath):
            os.makedirs(newpath);
     
         os.rename(filename,newpath+str(word1)+" - swb"+" - ("+name+") _"+str(xr)+".pdf")
    else:
        if(vod_percentage < 70 and vod_percentage >= 35):
          #filename1 = str.replace(filename2,"tags_","C");
          newpath = 'ClassifiedOutputFiles\\Vodafone\\';
          if not os.path.exists(newpath):
            os.makedirs(newpath);
     
          os.rename(filename,newpath+str(word1)+" - Vodafone"+" - ("+name+") "+"[c] _"+str(xr)+".pdf")
        elif (vod_percentage < 35):
           newpath = 'ClassifiedOutputFiles\\Not_recognized\\';
           if not os.path.exists(newpath):
              os.makedirs(newpath);

           os.rename(filename,newpath+str(word1)+" - Vodafone"+" - ("+name+") _"+str(xr)+".pdf")
        else:
         newpath = 'ClassifiedOutputFiles\\Vodafone\\';
         if not os.path.exists(newpath):
            os.makedirs(newpath);
     
         os.rename(filename,newpath+str(word1)+" - Vodafone"+" - ("+name+") _"+str(xr)+".pdf")
       
    ##tx=""
    ##for x in range(0, 3):
    ##    with open('train'+str(x+1)+'.txt', 'r') as f:
    ##        tx+=f.read()
    ##tx=tx.split("\n")
    ##new_tx=[]
    ##myDict1={}
    ##for word in tx:
    ##     if word in myDict1:
    ##          myDict1[word]+=1
    ##     else:
    ##         myDict1[word]=1
    ##for key,value in myDict1.items():
    ##    new_tx.append(key)
    ##new_tx.pop()
    ##new_tx.append('burgers')
    ##print ("Required words: ",new_tx)
    ##cv=[]
    ##xn=0
    ##for xc in new_tx:
    ##    if xn%2==0:
    ##        cv.append('hirsch')
    ##    else:
    ##        cv.append('swb')
    ##    xn=xn+1
    ##cv.pop()
    ##cv.append('check')
    ##    
    ##f_train=list(zip(new_tx, cv))
    ###print(f_train)
    ##cl = NaiveBayesClassifier(f_train)
    ##print(cl.classify("GESAMT"))

    ##sentence=nltk.tokenize.sent_tokenize(document)
    ##words=[nltk.word_tokenize(sent) for sent in sentence]
    ##
    ##new_words=(x for x in words if len(x)>2)
    ##print(new_words)
    #word_list=nltk.tokenize.word_tokenize(strn)

    ##word_list=strn.split(" ")
    ##print(word_list)
    ##myDict={}
    ##for word in word_list:
    ##     if word in myDict:
    ##          myDict[word]+=1
    ##     else:
    ##         myDict[word]=1
                

    ##for key,value in myDict.items():
    ##    print(key,value)

    ##fdist = FreqDist()
    ##for sentence in nltk.tokenize.sent_tokenize(strn):
    ##    for word in nltk.tokenize.word_tokenize(sentence):
    ##        fdist[word] += 1
    ##xp=""
    ##for sentence in nltk.tokenize.sent_tokenize(strn):
    ##    for word in nltk.tokenize.word_tokenize(sentence):
    ##        xp+=word+" "+str(fdist[word])+"\n"
    ##
    ##x=open('20160222 - Hirsch - Vertrag (Till) [tags_] [done]006049.txt','w')
    ##x.write(xp)
    ##x.close()
    ##        
            


