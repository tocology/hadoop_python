# hadoop_python

This repository is about programs of hadoop, expecially MapReduce programs.
Whole programs have been coded with Python.

## Development
### Preparation
Use python(<=2.7.10) and MRJob library
* MRJob library install (perhaps, you need administrator privilege)
```console
> pip install mrjob
```

We will use that library all the time. So, if you want to get more information, please go to following site.

> URL: <http://pythonhosted.org/mrjob/>

If you are using Windows, it is recommended to use Enthought Canopy in this lecture. (it looks like IDE for python; provide editor and consoles internally)

> URL: <https://www.enthought.com/products/canopy/>

### Data
Basically, all data have been placed respectively in '/data' directory before execution.

In this project, we will use data got from GroupLens. However, GroupLens data are too large to uploaded to GitHub because of data size. So, Please download from GroupLens or following below direction. Other data could be found /data dir.

* [Movielens](http://grouplens.org/datasets/movielens/ "Movielens")


```console
> wget http://files.grouplens.org/datasets/movielens/ml-100k.zip
```

** Large Data **

```console
> wget http://files.grouplens.org/datasets/movielens/ml-1m.zip
```

* Fake Friends data

> data/fakefriends.csv

* Weather data from the year 1800

> data/1800.csv

* Book data

> data/book.txt

* Order Amount by Customer data

> data/customer-orders.csv

* Marvel input data

> data/Marvel-Graph.txt
> data/Marvel-Names.txt

### Run
This lecture is dealing with how to make MapReduce(Mapper and Reducer) and implement real requirement like this project; Finding Movie Similarities, how much each movie has similarity with other movies.

Before running these programs, it is recommended to test and look up some small programs described in Test section.

* Finding Movie Similarities

**On Local**

```console
> python app/MovieSimilarities.py --items=data/ml-100k/u.item data/ml-100k/u.data > dist/moviesimilarities.txt
```
This program should need 15 mins depanding on your computer spec.
Additionally, you can know more commands; with EMR

**On EMR of Amazon Web Service**

If you want to run this program on EMR, command like below. it will move automatically. First of all, it is important that you have to set up system environment with Amazon Access and Secret keys on your OS before execution.
```console
> python app/MovieSimilarities.py -r emr --items=data/ml-100k/u.item data/ml-100k/u.data > dist/sims.txt
```

However, it will take more time to be finished then previous one; running on your own computer locally is faster because the spec of your machine seems better. So, we need more options like below. (with 4 instances)
```console
> python app/MovieSimilarities.py -r emr  --num-ec2-instances 4 --items=data/ml-100k/u.item data/ml-100k/u.data > dist/sims-4-machines.txt
```

**NOTE**

In fact, there are not 4 machines in working; The only 3 machines(Slave) are working, but one of them is Master controlling others.
And you should know that 3 machines made final result, so the each result of 3 reducers is not sorted when they are merged. So, you can see the result having 3 sections.

**How to Troubleshooting**

```console
> python app/MovieSimilarities.py -r emr --num-ec2-instances 4 --items=data/ml-100k/u.ITEM data/ml-100k/u.data > simsfail.txt
```

Looking above things, we're able to find that there is an error; u.ITEM is not same with u.item because uppercase letters are handled differently with lowercase ones except on Windows(Windows looks these two cases same).

At that time, we can get log from following command. [j-1NXMMBNEQHAFT] can be changed (it is EMR Cluster ID)

```console
> python -m mrjob.tools.emr.fetch_logs --find-failure [j-1NXMMBNEQHAFT]
```

**Scale Up for Large data**

We can execute this program for getting results within better time by increasing machines.

```console
python app/MovieSimilarities.py -r emr  --num-ec2-instances 20 --items=data/ml-100k/u.item data/ml-100k/u.data > dist/sims-20-machines.txt
```

### Test
* Rating Counter with ml-100k data
```console
> python app/RatingCounter.py data/ml-100k/u.data
```

* Average Friends by Age with Fake Friends data
```console
> python app/FriendsByAge.py data/fakefriends.csv
> python app/FriendsByAge.py data/fakefriends.csv > dist/friendsbyage.txt
```

* Finding Temperature Extremes

Get minimum temperature by location
```console
> python app/MinTemperatures.py data/1800.csv > dist/mintemps.txt
```

Get maximum temperature by location
```console
> python app/MaxTemperatures.py data/1800.csv > dist/maxtemps.txt
```

* Word Frequency

However, it still make some errors
```console
> python app/WordFrequency.py data/Book.txt > dist/wordcount.txt
```

Better version, but the order of results is weird
```console
> python app/WordFrequencyBetter.py data/Book.txt > dist/wordcountbetter.txt
```

Using chaining step method, results are sorted by the values(frequencies)
```console
> python app/WordFrequencySorted.py data/Book.txt > dist/wordcountsorted.txt
```

* Count Order Amount by Customer (homework)
```console
> python app/CustomerOrderAmount.py data/customer-orders.csv > dist/customerorders.txt
```

Implemented with sort
```console
> python app/CustomerOrderAmountSorted.py data/customer-orders.csv > dist/customerorderssorted.txt
```

Implemented with combiner
```console
> python app/CustomerOrderAmountCombiner.py data/customer-orders.csv > dist/customerorderscombiner.txt
```

* Most Popular Movie
```console
> python app/MostPopularMovie.py data/ml-100k/u.data > dist/mostpopularmovie.txt
```

Mapping Movie's name with the results
```console
> python app/MostPopularMovieNicer.py --items=data/ml-100k/u.item data/ml-100k/u.data > dist/mostpopularmovienicer.txt
```

* Most Popular SuperHero
```console
> python app/MostPopularSuperHero.py --names=data/Marvel-Names.txt data/Marvel-Graph.txt > dist/mostpopularsuperhero.txt
```

* Degrees of SuperHero

First, we need to make BFS of selected SuperHeroID; ex. 2548. Before execution,  'data/BFS-iteration-0.txt' file has to be created for results.
```console
> python app/ProcessMarvel.py 2548
```

Second, we run this program again and again util getting result.
```console
> python app/BFSIteration.py --target=100 data/BFS-iteration-0.txt > data/BFS-iteration-1.txt
> python app/BFSIteration.py --target=100 data/BFS-iteration-1.txt > data/BFS-iteration-2.txt
...
```
