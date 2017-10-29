package com.test;

import java.io.IOException;

import org.junit.Test;

import com.dt.Tools;

public class TestApp {

	@Test
	public void testPath() {
		String path = Tools.class.getResource("/").getPath();
		System.out.println(path);
	}
	
	@Test
	public void testLoadTxt() throws IOException {
		Tools.loadTxt();
	}
}
