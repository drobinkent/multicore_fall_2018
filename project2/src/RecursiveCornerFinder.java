package src;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

public class RecursiveCornerFinder extends RecursiveTask<float[]>{
	int start = 0;
	int end = 0;
	private CensusGroup[] totalData = null;
	int dataSize = 0;
	

	public  RecursiveCornerFinder(int start, int end, CensusGroup[] totalData, int dataSize) {
		this.start = start;
		this.end = end;
		this.totalData = totalData;
		this.dataSize = dataSize;
	}


	@Override
	public float[] compute(){
		if (end-start <= Utilities.CUTOFF_SIZE_V4 - 1){
			float north = Integer.MIN_VALUE;
			float south = Integer.MAX_VALUE;
			float east = Integer.MAX_VALUE;
			float west = Integer.MIN_VALUE;

			for (int i = start; i <= end; i++){
				CensusGroup group = this.totalData[i];
				//System.out.println(group.latitude);
				north = Math.max(north, group.latitude);
				south = Math.min(south, group.latitude);
				east = Math.min(east, group.longitude);
				west = Math.max(west, group.longitude);
			}
			float [] cornerPoints =  {north, south, east, west};
			return cornerPoints;
		}
		int mid = (start + end)/2;
		//System.out.println(mid);
		RecursiveCornerFinder left = new RecursiveCornerFinder(start, mid, this.totalData, dataSize);
		RecursiveCornerFinder right = new RecursiveCornerFinder(mid+1, end, this.totalData, dataSize);

		left.fork();
		float[] rightCorners = right.compute();
		float[] lefttCorners = left.join();


		float north = Math.max(rightCorners[0], lefttCorners[0]);
		float south = Math.min(rightCorners[1], lefttCorners[1]);
		float east = Math.min(rightCorners[2], lefttCorners[2]);
		float west = Math.max(rightCorners[3], lefttCorners[3]);
		float [] cornerPoints =  {north, south, east, west};
		return cornerPoints;	
	}

}
