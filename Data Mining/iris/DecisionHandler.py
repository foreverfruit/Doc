# 决策处理模块
import DataHandler as dh
from TreeNode import TreeNode as tn

def createDecisionTree(dataset:list):
    """
    决策树构造函数
    :param dataset:输入训练数据集
    :return: 返回当前决策树的root结点
    """
    pass
    return tn(None)

def testDecisonTree(dataset:list):
    """
    决策树测试函数
    :param dataset:输入测试集
    :return: 返回该模型针对这个测试集的一系列性能测试结果的列表
    """
    pass


def predict(data):
    """
    对一条数据做类型判定
    :param data: 输入一个列表类型数据（包含4个属性）
    :return: 返回该数据的类型
    """
    pass
    return 'type a'


if __name__ == '__main__':
    # 获取数据集
    trainset,testset = dh.loadData()
    # 获得每个属性的划分点
    devidePoints = dh.devidepoints(trainset)
    # 构造决策树
    root = createDecisionTree(trainset)
    # 测试该决策树
    # 需要改进，这里root返回的模型决策树是带着训练数据的，应该返回一棵只有结构没有数据的树
    # 预测数据
    result = predict([1,2,3,4])