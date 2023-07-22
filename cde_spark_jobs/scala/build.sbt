//scalafmtOnCompile in Compile := true

organization := "com.github.pdefusco"
name := "CDEJobJar"

version := "1.0"

scalaVersion := "2.12.15"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.2.3"

licenses := Seq("MIT" -> url("http://opensource.org/licenses/MIT"))

homepage := Some(url("https://github.com/pdefusco/CDE119_ACE_WORKSHOP"))
