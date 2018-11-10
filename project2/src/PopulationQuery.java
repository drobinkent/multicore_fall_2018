package src;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class PopulationQuery {
	// next four constants are relevant to parsing
	public static final int TOKENS_PER_LINE  = 7;
	public static final int POPULATION_INDEX = 4; // zero-based indices
	public static final int LATITUDE_INDEX   = 5;
	public static final int LONGITUDE_INDEX  = 6;
	public static double totalUsaPopulation = 0;
	// parse the input file into a large array held in a CensusData object
	public static CensusData parse(String filename) {
		CensusData result = new CensusData();
		BufferedReader fileIn = null;
        try {
        	fileIn = new BufferedReader(new FileReader(filename));
            
            // Skip the first line of the file
            // After that each line has 7 comma-separated numbers (see constants above)
            // We want to skip the first 4, the 5th is the population (an int)
            // and the 6th and 7th are latitude and longitude (floats)
            // If the population is 0, then the line has latitude and longitude of +.,-.
            // which cannot be parsed as floats, so that's a special case
            //   (we could fix this, but noisy data is a fact of life, more fun
            //    to process the real data as provided by the government)
            
            String oneLine = fileIn.readLine(); // skip the first line

            // read each subsequent line and add relevant data to a big array
            while ((oneLine = fileIn.readLine()) != null) {
                String[] tokens = oneLine.split(",");
                if(tokens.length != TOKENS_PER_LINE)
                	throw new NumberFormatException();
                int population = Integer.parseInt(tokens[POPULATION_INDEX]);
                if(population != 0)
                	result.add(population,
                			   Float.parseFloat(tokens[LATITUDE_INDEX]),
                		       Float.parseFloat(tokens[LONGITUDE_INDEX]));
                	totalUsaPopulation += population;
            }

            
        } catch(IOException ioe) {
            System.err.println("Error opening/reading/writing input or output file."+ioe);
            System.exit(1);
        } catch(NumberFormatException nfe) {
            System.err.println(nfe.toString());
            System.err.println("Error in file format");
            System.exit(1);
        }finally {
        	try {
				fileIn.close();
			} catch (IOException e) {
				System.err.println("Error closing input or output file.");
	            System.exit(1);
			}
        }
        return result;
	}

	// argument 1: file name for input data: pass this to parse
	// argument 2: number of x-dimension buckets
	// argument 3: number of y-dimension buckets
	// argument 4: -v1, -v2, -v3, -v4, or -v5
	public static void main(String[] args) {
		// FOR YOU
	}

	public static Pair<Integer, Float> singleInteraction(int w, int s, int e, int n, int versionNum) {
		// TODO Auto-generated method stub
		Pair< Integer, Float> queryResult  = null;
		
		
		switch(versionNum) {
		
			case 1:
				queryResult = getQueryResulV1(w,s,e,n);
				break;
			case 2:
				break;
			case 3:
				//This version is a sequential one but it needs som preprocessing. We need to answer the query from preprocessed data
				
				break;
			case 4:
				break;
			case 5:
				break;
			default:
				System.out.println("Wrong version number-"+versionNum+"priveded. Exiting!!!");
				System.exit(0);
		}
		return queryResult;
	}

	
	/*
	 * Thjis function checks each of the data point  
	 * Then if the point's index belongs to the given w,s,e,n box then ad it to query answer.
	 * Otherwise leave it
	 */
	private static Pair< Integer, Float> getQueryResulV1(int w, int s, int e, int n) {
		float[] cornerPoints = Utilities.findCorner(PopulationQuery.totalCensusData);
		int totalPopulationInQueryRange = 0;
		for(int i = 0; i < PopulationQuery.totalCensusData.data_size; i++) {
			CensusGroup group = PopulationQuery.totalCensusData.data[i];
			int[] index = Utilities.findIndex(group.longitude, group.latitude, cornerPoints, 
					PopulationQuery.columns, PopulationQuery.rows);
			//if indexes fall inside w,s,e,n 
			//totalPopulation += group.population;
			
			if(( index[1] >= w) &&(( index[1] <= e)) &&
					(index[0] >= s) && ( index[0]<= n)) {
				totalPopulationInQueryRange += group.population;
				
			}
		}
		return new Pair<Integer, Float>(totalPopulationInQueryRange, (float)(totalPopulationInQueryRange/PopulationQuery.totalUsaPopulation));
	}



	///Data related to preprocessing
	private static CensusData totalCensusData= null;  //In this object all the datas parsed from the input file will be kept
	private  static int[][] totalPopulationInEachBiggerRectangle;
	private static int columns, rows;
	
	
	/*
	 * Here we will read the given file and store the data in a CensusDAta object. 
	 * Then for each version we will store the processed data in a single object. 
	 * Then when each time a new query comes we will serve the query based in that data
	 */
	public static void preprocess(String filename, int columns, int rows, int versionNum) {

		//initialize data structures where pricessed data will be kept for answering queries
		PopulationQuery.columns = columns;
		PopulationQuery.rows = rows;
		System.out.println("File name is "+ filename);
		if(PopulationQuery.totalCensusData ==null)
			PopulationQuery.totalCensusData = PopulationQuery.parse(filename);
		if(totalPopulationInEachBiggerRectangle == null)
			totalPopulationInEachBiggerRectangle = new int[rows][columns];

		System.out.println("Total number of rows parsed from the file is : "+ PopulationQuery.totalCensusData.data_size);
		PopulationQuery pq = new PopulationQuery();
		switch(versionNum) {
		
			case 1:
				/*
				 * Truly speaking I don't see any necessity of preprocessing in version 1.
				 * Just answer the query and bang!!
				 */
				break;
			case 2:
				break;
			case 3:
				float[] cornerPoints = Utilities.findCorner(PopulationQuery.totalCensusData);
				pq.findPopulationInEachBiggerRectagnle( rows,columns,  cornerPoints);
				pq.preprocessV3();
				break;
			case 4:
				break;
			case 5:
				break;
			default:
				System.out.println("Wrong version number-"+versionNum+"priveded. Exiting!!!");
				System.exit(0);
		}
		
		
	}

	/*
	 * This method calcutes total population in the bigger rectangles starting from origin (0,0) 
	 * origin is bottommost leftmost corner in the grid
	 */
	private  void preprocessV3() {
		// TODO Auto-generated method stub
		int row = totalPopulationInEachBiggerRectangle.length;
		int col = totalPopulationInEachBiggerRectangle[0].length;

		for (int j = 1; j < col; j++){
			totalPopulationInEachBiggerRectangle[row - 1][j] = totalPopulationInEachBiggerRectangle[row - 1][j - 1] + totalPopulationInEachBiggerRectangle[row - 1][j];
		}
		for (int i = row - 2; i >= 0; i--){
			totalPopulationInEachBiggerRectangle[i][0] = totalPopulationInEachBiggerRectangle[i + 1][0] + totalPopulationInEachBiggerRectangle[i][0];
		}
		//step2: dp main algorithm
		for (int i = row - 2; i >= 0; i--){
			for (int j = 1; j < col; j++){
				totalPopulationInEachBiggerRectangle[i][j] = totalPopulationInEachBiggerRectangle[i + 1][j] + 
						totalPopulationInEachBiggerRectangle[i][j - 1] - totalPopulationInEachBiggerRectangle[i + 1][j - 1] +
						totalPopulationInEachBiggerRectangle[i][j];
			}
		}
		
	}

	
	/*
	 * In this method we only compute total pooulation in a bigger rectangle
	 */
	private  void findPopulationInEachBiggerRectagnle(int columns, int rows, float[] cornerPoints) {

		for(int i = 0; i < PopulationQuery.totalCensusData.data_size; i++) {
			CensusGroup group = PopulationQuery.totalCensusData.data[i];
			int[] index = Utilities.findIndex(group.longitude, group.latitude, cornerPoints, columns, rows);
			int rowNum = index[0];
			int colNum = index[1];
			if (rowNum == rows && colNum == columns){
				totalPopulationInEachBiggerRectangle[rowNum - 1][colNum - 1] += group.population;
			}else if (rowNum == rows){
				totalPopulationInEachBiggerRectangle[rowNum - 1][colNum] += group.population;
			}else if (colNum == columns){
				totalPopulationInEachBiggerRectangle[rowNum][colNum - 1] += group.population;
			}else{
				totalPopulationInEachBiggerRectangle[rowNum][colNum] += group.population;
			}
			//totalPopulation += group.population;
		}
		
	}
}
