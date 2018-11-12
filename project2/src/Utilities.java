package src;

public class Utilities {
	
	public static int CUTOFF_SIZE_V2 =5000; 
	public static int CUTOFF_SIZE_V4 =100; 
	public static int CUTOFF_SIZE_V5 =100; 
	public static int TOTAL_THREADS =4; 


	
	/*
	 * This function iterates over a given set of Census Data and finds what are the corners of those data
	 */
	
	public static float[] findCorner(CensusData censusData) {
		
		float upperMost = Integer.MIN_VALUE;
		float LowerMost = Integer.MAX_VALUE;
		float leftMost = Integer.MAX_VALUE;
		float rightMost = Integer.MIN_VALUE;
		for (int i = 0; i < censusData.data_size; i++){
			CensusGroup group = censusData.data[i];
			upperMost = Math.max(upperMost, group.latitude);
			LowerMost = Math.min(LowerMost, group.latitude);
			leftMost = Math.min(leftMost, group.longitude);
			rightMost = Math.max(rightMost, group.longitude);
		}

		return new float[]{upperMost, LowerMost, leftMost, rightMost};
	}

	/*
	 * This function finds the location of  a given longitude and lattitude whre the location is bounded by 4 corners.
	 * This 4 corners essentially gives the dimension of a 2 d array
	 * Return a 1 d array of size. 1st one gives the row and 2 nd one gives the column 
	 * this row and column represnts the index of a census Data point in the rectangle we are divinding the whole USA map
	 */
	public static  int[] findIndex(float longitude, float latitude, float[] corners, int cols, int rows) {
		float top = corners[0];
		float bottom = corners[1];
		float left = corners[2];
		float right = corners[3];

		float height = (top - bottom)/rows;
		float width = (right - left)/cols;

		int[] index = new int[2];
		index[0] = (int)((latitude-bottom)/height);
		index[1] = (int)((longitude-left)/width);
		return index;
	}
	
	
}
