import  os

class utils:

    @staticmethod
    def getPath():
        """返回项目根目录"""
        return os.path.abspath('..')
