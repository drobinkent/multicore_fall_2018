package src;

import java.util.concurrent.locks.Lock;

public class ThreadBasedGridBuilderForV5 extends Thread {

	int start = 0;
	int end = 0;
	private CensusGroup[] totalData = null;
	int dataSize = 0;
	int columns = 0;
	int rows = 0;
	float[] cornerPoints;
	Lock lock;

	public ThreadBasedGridBuilderForV5(int start, int end, CensusGroup[] totalData, int dataSize, int columns, int rows,
			float[] cornerPoints, Lock lock) {
		this.start = start;
		this.end = end;
		this.totalData = totalData;
		this.dataSize = dataSize;
		this.columns = columns;
		this.rows = rows;
		this.cornerPoints = cornerPoints;
		this.lock = lock;
		System.out.println("Inside ThreadBasedGridBuilderForV5: start = "+this.start+" ENd : "+this.end);
	}

	public void run() {
		int totalPopulation = 0;
		for (int i = start; i < end; i++) {
			CensusGroup group = PopulationQuery.totalCensusData.data[i];
			int[] index = Utilities.findIndex(group.longitude, group.latitude, cornerPoints, columns, rows);
			int rowNum = index[0];
			int colNum = index[1];
			try {
				lock.lock();
//				if (rowNum == rows && colNum == columns) {
//					PopulationQuery.totalPopulationInEachBiggerRectangle[rowNum - 1][colNum - 1] += group.population;
//				} else if (rowNum == rows) {
//					PopulationQuery.totalPopulationInEachBiggerRectangle[rowNum - 1][colNum] += group.population;
//				} else if (colNum == columns) {
//					PopulationQuery.totalPopulationInEachBiggerRectangle[rowNum][colNum - 1] += group.population;
//				} else {
////					System.out.println("Total column : "+columns+ " -- Total row : "+rows);
////					System.out.println("Current data points column : "+colNum+ " --  row : "+rowNum);
//
//					PopulationQuery.totalPopulationInEachBiggerRectangle[rowNum][colNum] += group.population;
//				}
				PopulationQuery.totalPopulationInEachBiggerRectangle[rowNum][colNum] += group.population;
				//PopulationQuery.totalUsaPopulation += group.population;
			}catch(Exception e ) {
				System.out.println("Exception in thread based population grid builder"+e.toString());
			}finally {
				lock.unlock();
			}
			
		}
	}
}
