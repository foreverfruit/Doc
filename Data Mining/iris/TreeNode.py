# 树节点
class TreeNode(object):
    """
    树节点
    """
    def __init__(self,dataset:[]):
        # 本结点的三个子节点
        self.children=[]

        # 本节点的数据集合
        self.data = dataset
        # 当前结点类型为数据集合中多的那一类的类标号
        self.classlabel=''
        # 结点类型，0为非叶结点，1为页结点
        self.nodetype = 0

        # 该结点的划分属性
        self.devideAttr=''
        # 该节点的属性划分点
        self.devidePoints=()

    def insert(self,node:TreeNode):
        """插入结点到指定的位置"""
        self.children.append(node)

    def findAttr(self):
        """
        根据当前结点的数据集寻找最佳划分的属性
        对比三种属性的划分后的Gini指数，选择最佳的划分属性
        返回属性标号:DataHandler.attrlabel中的一个值
        """
        pass

    def findPoints(self):
        """
        因为每个属性都是离散的，且根据数据集特点需要做3段划分，这里需要找到两个划分点
        根据数据的分布密度来划分，已知类型总量为3，假设该属性会集中分布到三个区域，
        找到这三个区域的两个边界即可
        """
        pass
        return (1,2)

    def devide(self,attr='',point=()):
        """
        就是根据属性测试条件，以及测试点，将数据集合分成几个部分，分别建立TreeNode然后加入子节点集合
        返回子节点集合
        """
        pass
        return (1,2,3)

    def checkDevideEnd(self):
        """
        两个划分结束判断：
        1. 数据集合的属性集合相同（离散情况下就是所有实体的每个属性都在相同的划分区间）
        2. 数据集中的90%的实体是同一个类标号
        """
        pass
        return True

