import org.apache.spark.sql.SparkSession

object ExampleApp {
  def main(args: Array[String]): Unit = {
    // create SparkSession
    val spark = SparkSession.builder()
      .appName("MapExample")
      .master("local[*]")
      .getOrCreate()

    // create an RDD with some data
    val data = spark.sparkContext.parallelize(Seq(1, 2, 3, 4, 5))

    // apply map function to RDD to double each element
    val doubled = data.map(x => x * 2)

    // print the result
    doubled.collect().foreach(println)

    // stop the SparkSession
    spark.stop()
  }
}
