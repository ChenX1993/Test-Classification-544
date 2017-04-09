# -- coding: utf-8 --
#!/usr/bin/python
import codecs
import math
import os
from sys import maxsize 

def sim(test_dic, train_dic, dicFeature):  #test_dic--样本列表
    b = 0.0 
    c1 = 0.0  
    c2 = 0.0
    sim = 0.0

    for index in dicFeature: 
        if index not in test_dic:
            x = 0.0
        else:
             x = float(test_dic[index])
        if index not in train_dic:
            y = 0.0
        else:
            y = float(train_dic[index])

        b += x * y
        c1 += math.pow(x, 2)  
        c2 += math.pow(y, 2) 

    if (math.sqrt(c1) * math.sqrt(c2) == 0):
        sim = 0.0
    else:
        sim = b / (math.sqrt(c1) * math.sqrt(c2)) #cos值
    return sim  
 
def classify(k, docWeight, testWeight, dicFeature):  
    result = list()
    for key in testWeight:

        li = list()
        test_lable = testWeight[key][0]#待分类文档类别
        test_dic = testWeight[key][1]

        
        for doc_key in docWeight: 

            train_lable = docWeight[doc_key][0]
            train_dic = docWeight[doc_key][1]
            s = sim(test_dic, train_dic, dicFeature)
            li.append((s,test_lable,train_lable)) 
        
        li.sort(reverse = True) #排序
#        print li
        tmpli = li[0:int(k)]         #取前k个

        di = dict()
        for l in tmpli: #遍历K个邻居
            s,test_lable,train_lable = l 
            if int(train_lable)in di:
                  di[int(train_lable)] += 1  
            else:
                di[int(train_lable)] = 1
            
        sortDi = sorted(di.items(),None, key=lambda d: d[1], reverse = True) #排序取文档数最多的类
#        print sortDi
        result_lable = sortDi[0][0]
        # print di
        result.append((int(result_lable), int(test_lable)))
#        print result
    return result


def main():
    file_path = "knn/model/train.svm"
    fileText_path = "knn/model/test.svm"

    weightDoc = list()
    docWeight = dict()

    weigthTest = list()  
    testWeight = dict()

    dicFeature = dict()

    docId = 1
    with open("knn/model/KNNeature.txt", "r") as f_in:
        lines = f_in.readlines()
        for line in lines:
            feature = line.strip().split(' ')
            dicFeature[feature[0]] = feature[1]
        # print dicFeature
    length = len(dicFeature)

    with open(file_path, "r") as f_in:
        lines = f_in.readlines()
        for line in lines:    
            feature = list()
            dicDoc = dict()
            weightDoc = line.strip().split(' ')
            if (len(weightDoc) > 1):
                feature.append(weightDoc[0]) #weight[0] -- label;

                for i in range(1,len(weightDoc)): #weight[1:] -- f_id:idf
                    if (weightDoc[i] != ''):
                        element = weightDoc[i].strip('\n').split(':') #element -- [f_id, idf]
                        dicDoc[element[0]] = element[1]

                feature.append(dicDoc)
                docWeight[docId] = feature  # docWeight{id : [lable, {f_id : idf}]}
                docId += 1


    testId = 1
    with open(fileText_path, "r") as f_in:
        lines = f_in.readlines()
        testLen = 0
        for line in lines:
            feature = list()
            dicTest = dict()
            weigthTest = line.strip('\n').split(' ')

            if (len(weigthTest) > 1):
                feature.append(weigthTest[0]) #weight[0] -- label;
                for i in range(1,len(weigthTest)): #weight[1:] -- f_id:idf
                    if (weigthTest[i] != ''):
                        element = weigthTest[i].strip('\n').split(':') #element -- [f_id, idf]
                        dicTest[element[0]] = element[1]

                feature.append(dicTest)
                testWeight[testId] = feature  # testWeight{id : [lable, {f_id : idf}]}

                testId += 1
    # print testWeight

    k = math.floor(math.sqrt(docId -1))

    tupleReuslt = classify(k, docWeight, testWeight, dicFeature)
    # print tupleReuslt
    correct = 0
    total = 0
    correct = 0
    P_correct =0.0
    predictions = []

    TP = 0
    FP = 0
    FN = 0

    for e in tupleReuslt:
        total += 1
        result_label = int(e[0])
        test_label = int(e[1])
        predictions.append(result_label)
        if(int(e[0]) == int(e[1])):
            correct += 1
        if result_label == 1:
            if test_label == 1:
                TP += 1
            else:
                FP += 1
        elif test_label == 1:
            FN += 1
    P = float(TP) / (TP + FP)
    R = float(TP) / (TP + FN)
    F1 = 2.0 * P * R / (P + R)
    P_correct = float(correct) / float(total) 
    print "Accuracy:", P_correct, "K值:", k
    print "F1 Score:", F1


main()
