# 数据相关内容

# 这里类标号直接根据数据集写死了，不再设置通用的检测函数，同理属性集也一样
classlabel = ('Iris-setosa','Iris-versicolor','Iris-virginica')
attrlabel = ('sepal length','sepal width','petal length','petal width')

def loadData():
    """
    加载数据,返回训练集和测试集
    """
    trainingset,testset = [],[]

    with open('iris.data','r') as f:
        data = f.readlines()
        for i,e in enumerate(data):
            # 去掉行末的换行符
            e = e.strip('\n')
            # 将数据分割成列表
            e = e.split(',')
            # 2:1的比例分发数据到训练集和测试集，即分别100个和50个数据
            if(i%3):
                testset.append(e)
            else:
                trainingset.append(e)

    return trainingset,testset

if __name__ == '__main__':
    train,test = loadData()
    print(train)
    print(test)