package com.dt;
/**
 * 记录模型
 * @author Administrator
 *
 */
public class Record {
	
	private float sepal_length;
	private float sepal_width;
	private float petal_length;
	private float petal_width;
	private String catagory;
	
	public Record() {
		
	}
	
	public Record(float sepal_length, float sepal_width, float petal_length, float petal_width) {
		this.sepal_length = sepal_length;
		this.sepal_width = sepal_width;
		this.petal_length = petal_length;
		this.petal_width = petal_width;
	}
	
	public Record(float sepal_length, float sepal_width, float petal_length, float petal_width, String catagory) {
		this.sepal_length = sepal_length;
		this.sepal_width = sepal_width;
		this.petal_length = petal_length;
		this.petal_width = petal_width;
		this.catagory = catagory;
	}

	public float getSepal_length() {
		return sepal_length;
	}

	public float getSepal_width() {
		return sepal_width;
	}

	public float getPetal_length() {
		return petal_length;
	}

	public float getPetal_width() {
		return petal_width;
	}

	public String getCatagory() {
		return catagory;
	}
	
}
