package com.test;

import java.io.IOException;
import java.net.URISyntaxException;

import org.junit.Test;

import com.dt.Tools;

public class TestApp {

	@Test
	public void testPath() throws URISyntaxException {
		String path = Tools.class.getResource("/").toURI().getPath();
		System.out.println(path);
	}
	
	@Test
	public void testLoadTxt() throws IOException, URISyntaxException {
		Tools.loadTxt();
	}
}
