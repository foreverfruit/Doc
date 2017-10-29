package com.dt;

/**
 * 数据集管理对象
 * @author Administrator
 *
 */
public class DataSetManager {

	// 单例的管理对象
	private static DataSetManager instance; 
	private DataSet trainSet;
	private DataSet testSet;
	
	private DataSetManager() {
	}
	
	public static DataSetManager getDataSetManager() {
		if(instance==null) {
			instance = new DataSetManager();
		}
		return instance;
	}

	public DataSet getTrainSet() {
		return trainSet;
	}

	public void setTrainSet(DataSet trainSet) {
		this.trainSet = trainSet;
	}

	public DataSet getTestSet() {
		return testSet;
	}

	public void setTestSet(DataSet testSet) {
		this.testSet = testSet;
	}
	
}
