package src;

import java.util.concurrent.RecursiveTask;

public class RecursivePopulationFinderV2 extends RecursiveTask<Integer> {
	int start = 0;
	int end = 0;
	private CensusGroup[] totalData = null;
	int dataSize = 0;
	int columns = 0;
	int rows = 0;
	float[] cornerPoints;
	int w ,s,e,n;
	

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
	public  RecursivePopulationFinderV2(int start, int end, CensusGroup[] totalData, int dataSize, int columns,
			int rows, float[] cornerPoints, int w, int s, int e, int n) {
		this.start = start;
		this.end = end;
		this.totalData = totalData;
		this.dataSize = dataSize;
		this.columns = columns;
		this.rows = rows;
		this.cornerPoints = cornerPoints;
		this.w = w;
		this.s= s;
		this.e = e;
		this.n = n;

	}

	@Override
	protected Integer compute() {
		// This is the base case when no more divide and coinquers is needed.
		Integer totalPopulationInQueryRange  = 0;
		if (end- start <= Utilities.CUTOFF_SIZE_V2 - 1) {
			for (int i = start; i <= end; i++) {
				CensusGroup group = this.totalData[i];
				int[] index = Utilities.findIndex(group.longitude, group.latitude, cornerPoints, 
						this.columns, this.rows);
				//if indexes fall inside w,s,e,n 
				//totalPopulation += group.population;
				
				if(( index[1] >= w) &&(( index[1] <= e)) &&
						(index[0] >= s) && ( index[0]<= n)) {
					totalPopulationInQueryRange += group.population;
					
				}
			}
			return totalPopulationInQueryRange;
		}
		// divide
		int mid = (start + end) / 2;
		RecursivePopulationFinderV2  leftThread = new RecursivePopulationFinderV2( start, mid, totalData, dataSize, columns,
				rows, cornerPoints, w, s,  e, n) ;
		RecursivePopulationFinderV2  rightThread = new RecursivePopulationFinderV2( mid+1, end, totalData, dataSize, columns,
				rows, cornerPoints, w, s,  e, n) ;
		// conquer
		leftThread.fork();
		//rightThread.fork();
		int totalPopulationInRight = rightThread.compute();
		int totalPopulationInLEft = leftThread.join();
		totalPopulationInQueryRange  = totalPopulationInLEft+totalPopulationInRight;

		System.out.println("Inside version 2| left start "+this.start+"|end:  "+mid+" int totalPopulationInQueryRange ="+totalPopulationInQueryRange);
		System.out.println("Inside version 2| right start "+(mid+1)+"|end:  "+this.end+" int totalPopulationInQueryRange ="+totalPopulationInQueryRange);

		System.out.println("Inside version 2| start "+this.start+"|end:  "+this.end+" int totalPopulationInQueryRange ="+totalPopulationInQueryRange);
		if((this.start == 0 ) && (this.end == this.dataSize))
		{
			System.out.println("Reached to end");
		}
		return totalPopulationInQueryRange;
	}
}
