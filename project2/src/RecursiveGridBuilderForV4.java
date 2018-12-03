package src;

import java.util.concurrent.RecursiveTask;

public class RecursiveGridBuilderForV4 extends RecursiveTask<Pair<Integer, int[][]>> {
	int start = 0;
	int end = 0;
	private CensusGroup[] totalData = null;
	int dataSize = 0;
	int columns = 0;
	int rows = 0;
	float[] cornerPoints;


	/**
	 * 
	 * @param start
	 * @param end
	 * @param totalData
	 * @param dataSize
	 * @param columns
	 * @param rows
	 * @param cornerPoints
	 */
	public RecursiveGridBuilderForV4(int start, int end, CensusGroup[] totalData, int dataSize, int columns, int rows,
			float[] cornerPoints) {
		this.start = start;
		this.end = end;
		this.totalData = totalData;
		this.dataSize = dataSize;
		this.columns = columns;
		this.rows = rows;
		this.cornerPoints = cornerPoints;
	

	}

	@Override
	protected Pair<Integer, int[][]> compute() {
		// This is the base case when no more divide and conquers is needed.
		Integer totalPopulationInQueryRange = -1;
		int totalPopulation = 0;
		if (end - start <= Utilities.CUTOFF_SIZE_V2 - 1) {
			int[][] return_result = new int[this.rows][this.columns];
			for (int i = start; i <= end; i++) {
				CensusGroup group = this.totalData[i];
				int[] index = Utilities.findIndex(group.longitude, group.latitude, cornerPoints, columns, rows);
				int rowNum = index[0];
				int colNum = index[1];
//				if (rowNum == rows && colNum == columns) {
//					return_result[rowNum - 1][colNum - 1] += group.population;
//				} else if (rowNum == rows) {
//					return_result[rowNum - 1][colNum] += group.population;
//				} else if (colNum == columns) {
//					return_result[rowNum][colNum - 1] += group.population;
//				} else {
////				System.out.println("Total column : "+columns+ " -- Total row : "+rows);
////				System.out.println("Current data points column : "+colNum+ " --  row : "+rowNum);
//					return_result[rowNum][colNum] += group.population;
//				}
				return_result[rowNum][colNum] += group.population;
				totalPopulation += group.population;
			}
			return new Pair<Integer, int[][]>(totalPopulation, return_result);
		}

		// divide
		int mid = (start + end) / 2;
		RecursiveGridBuilderForV4 left = new RecursiveGridBuilderForV4(start, mid, totalData, dataSize,columns, rows, cornerPoints);
		RecursiveGridBuilderForV4 right =  new RecursiveGridBuilderForV4(mid+1, end, totalData, dataSize,columns, rows, cornerPoints);
		//conquer
		left.fork();
		Pair<Integer, int[][]> rightPair = right.compute();
		Pair<Integer, int[][]> leftPair = left.join();
		int result = rightPair.getElementA() + leftPair.getElementA();
		int[][] return_result = leftPair.getElementB();
		for (int i = 0; i < return_result.length; i++){
			for (int j = 0; j < return_result[0].length; j++){
				return_result[i][j] += rightPair.getElementB()[i][j];
			}
		}

		return new Pair<Integer, int[][]>(result, return_result);
	}

}
