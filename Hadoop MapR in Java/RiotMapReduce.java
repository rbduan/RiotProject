// Dongyeop Duke Lee
// MapReduce to find Average game length / cs / kill / death per team per game


import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;



public class RiotMapReduce{
	
	public static class GameData implements WritableComparable<GameData> {
		IntWritable gameLength;
		IntWritable win_total_cs;
		IntWritable win_total_kill;
		IntWritable lose_total_cs;
		IntWritable lose_total_kill;
		
		public GameData() {
			set(new IntWritable(0), new IntWritable(0), new IntWritable(0), new IntWritable(0), new IntWritable(0));
		}
		
		public GameData(int leng, int wincs, int winkill, int losecs, int losekill) {
			set(new IntWritable(leng), new IntWritable(wincs), new IntWritable(winkill), new IntWritable(losecs), new IntWritable(losekill));
		}
		
		public void set(IntWritable leng, IntWritable wincs, IntWritable winkill, IntWritable losecs, IntWritable losekill) {
			this.gameLength = leng;
			this.win_total_cs = wincs;
			this.win_total_kill = winkill;
			this.lose_total_cs = losecs;
			this.lose_total_kill = losekill;
		}
		
		public IntWritable getLength() {
			return gameLength;
		}
		public IntWritable getWinCs() {
			return win_total_cs;
		}
		public IntWritable getWinKill() {
			return win_total_kill;
		}
		public IntWritable getLoseCs() {
			return lose_total_cs;
		}
		public IntWritable getLoseKill() {
			return lose_total_kill;
		}
		
		public void setGameLength(int leng) {
			this.gameLength = new IntWritable(leng);
		}
		public void setWinCs(int wincs) {
			this.win_total_cs = new IntWritable(wincs);
		}
		public void setWinKill(int winkill) {
			this.win_total_kill = new IntWritable(winkill);
		}
		public void setLoseCs(int losecs) {
			this.lose_total_cs = new IntWritable(losecs);
		}
		public void setLoseKill(int losekill) {
			this.lose_total_kill = new IntWritable(losekill);
		}
		

		@Override
		public void readFields(DataInput arg0) throws IOException {
			// TODO Auto-generated method stub
			gameLength.readFields(arg0);
			win_total_cs.readFields(arg0);
			win_total_kill.readFields(arg0);
			lose_total_cs.readFields(arg0);
			lose_total_kill.readFields(arg0);
			
			
		}

		@Override
		public void write(DataOutput arg0) throws IOException {
			// TODO Auto-generated method stub
			gameLength.write(arg0);
			win_total_cs.write(arg0);
			win_total_kill.write(arg0);
			lose_total_cs.write(arg0);
			lose_total_kill.write(arg0);
			
		}

		@Override
		public int compareTo(GameData o) {
			// TODO Auto-generated method stub
			return 0;
		}
		
	}
	
	public static class RiotMap extends Mapper<LongWritable, Text, Text, GameData>{
		
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			//from business
			String delims = "^";
			String[] businessData = StringUtils.split(value.toString(),delims);
			int leng = 0;
			int wincs=0;
			int winkill=0;
			int losecs=0;
			int losekill=0;
			if (businessData.length ==42) {
				leng = Integer.parseInt(businessData[1]);
				
				for (int i=0; i<10; i++) {
					if (i<5) { // winning team
 						wincs += Integer.parseInt(businessData[i*4+2]);
 						winkill += Integer.parseInt(businessData[i*4+3]);
					}
					else {
						losecs += Integer.parseInt(businessData[i*4+2]);
						losekill += Integer.parseInt(businessData[i*4+3]);
					}
					//context.write(new Text(businessData[0]), new IntWritable(Integer.parseInt(businessData[i*4+2])));
				}
				GameData gd = new GameData();
				gd.set(new IntWritable(leng), new IntWritable(wincs), new IntWritable(winkill), new IntWritable (losecs), new IntWritable(losekill));
				context.write(new Text(businessData[0]),  gd);
			}		
		}
	
		@Override
		protected void setup(Context context)
				throws IOException, InterruptedException {
		}
	}

	public static class RiotReduce extends Reducer<Text, GameData,Text,Text> {
		
		private int sum_win_cs=0;
		private int sum_win_kill=0;
		private int sum_lose_cs=0;
		private int sum_lose_kill=0;
		private int sum_game_length=0;
		private int count=0;
		public void reduce(Text key, Iterable<GameData> values,Context context ) throws IOException, InterruptedException {


			for (GameData gd : values) {
				sum_game_length += gd.getLength().get();
				sum_win_cs += gd.getWinCs().get();
				sum_win_kill += gd.getWinKill().get();
				sum_lose_cs += gd.getLoseCs().get();
				sum_lose_kill += gd.getLoseKill().get();
			}
			count++;
			//context.write(key, iw);
		}

		@Override
		public void cleanup(Context context) throws IOException, InterruptedException {
			String output = "Avg Length: " + Integer.toString(sum_game_length/count);
			output += "\nAvg Win CS: " + Integer.toString(sum_win_cs/count);
			output += "\nAvg Win Kill: " + Integer.toString(sum_win_kill/count);
			output += "\nAvg Lose CS: " + Integer.toString(sum_lose_cs/count);
			output += "\nAvg Lose Kill: " + Integer.toString(sum_lose_kill/count);
			
			context.write(new Text("Game Length"), new Text(output));
			
			//context.write(new Text(Integer.toString(count_ins) + " " + Integer.toString(count)), new Text("Avg Game Length: " + Integer.toString(sum_game_length) + "\nAvg Win CS: " + Integer.toString(sum_win_cs/count) + "\nAvg Win Kill: " + Integer.toString(sum_win_kill/count) + "\nAvg Lose CS: " + Integer.toString(sum_lose_cs/count) + "\nAvg Lose Kill: " + Integer.toString(sum_lose_kill/count)));
			
			
			//context.write(new Text("total"), new Text(Integer.toString(count_ins)+" "+Integer.toString(count)+" "+Integer.toString(sumcs/count)));
		}
	}

	
	
	
// Driver program
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();		// get all args
		if (otherArgs.length != 2) {
			System.err.println("Usage: RiotMapReduce <in> <out>");
			System.exit(2);
		}
			  
		Job job = Job.getInstance(conf, "RiotMapReduce");
		job.setJarByClass(RiotMapReduce.class);
		
		job.setMapperClass(RiotMap.class);
		job.setReducerClass(RiotReduce.class);
		job.setNumReduceTasks(1);
		//uncomment the following line to add the Combiner
		//job.setCombinerClass(Reduce.class);
		
		// set output key type 
		
		job.setOutputKeyClass(Text.class);
		job.setMapOutputKeyClass(Text.class);
		
		// set output value type
		job.setMapOutputValueClass(GameData.class);
		job.setOutputValueClass(Text.class);
		
		
		//set the HDFS path of the input data
		FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		// set the HDFS path for the output 
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
		
		//Wait till job completion
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}

	
	