package com.dt;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URISyntaxException;

public class Tools {

	/**
	 * 加载项目data目录下的data文件，自动分发到两个数据集
	 * @throws IOException 
	 * @throws URISyntaxException 
	 */
	public static void loadTxt() throws IOException, URISyntaxException {
		String path = Tools.class.getResource("/").toURI().getPath();
		File file = new File(path,"iris.data");
		BufferedReader br = new BufferedReader(new FileReader(file));
		String temp;
		int i = 0;
		while((temp = br.readLine())!=null) {
			i++;
			System.out.println(i + ":" + temp);
		}
		
		br.close();
	}
}
