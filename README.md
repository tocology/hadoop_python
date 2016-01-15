# hadoop_python
This project for udemy lecture; Taming Big Data with MapReduce and Hadoop

## Development
### Preparation
Use python(<=2.7.10) and MRJob library
* MRJob library install (perhaps, you need administrator privilege)
```console
> pip install mrjob
```

If you are using Windows, it is recommended to use Enthought Canopy in this lecture. (it looks like IDE for python; provide editor and consoles internally)

> URL: <https://www.enthought.com/products/canopy/>

### Data
Basically, all data have been placed respectively in '/data' directory before execution.

* [Movielens](http://grouplens.org/datasets/movielens/ "Movielens")

In this project, we use ml-100k

```console
> wget http://files.grouplens.org/datasets/movielens/ml-100k.zip
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
python app/ProcessMarvel.py 2548
```

Second, we run this program again and again util getting result.
```console
> python app/BFSIteration.py --target=100 data/BFS-iteration-0.txt > data/BFS-iteration-1.txt
> python app/BFSIteration.py --target=100 data/BFS-iteration-1.txt > data/BFS-iteration-2.txt
...
```

* Finding Similar Movies
```console
> python app/MovieSimilarities.py --items=data/ml-100k/u.item data/ml-100k/u.data > dist/moviesimilarities.txt
```
This program should need 15 mins depanding on your computer spec.
Additionally, you can know more commands; with EMR

If you want to run this program on EMR, command like below. it will move automatically. However, it is important that you have to set up system environment with Amazon Access and Secret keys on your OS before execution.
```console
python app/MovieSimilarities.py -r emr --items=data/ml-100k/u.item data/ml-100k/u.data > dist/sims.txt
```

However, it will cost more time to finished then previous one; run on your own computer locally because the only one machine moved on. So, we need more options like below. (with 4 instances)
```console
python app/MovieSimilarities.py -r emr  --num-ec2-instances 4 --items=data/ml-100k/u.item data/ml-100k/u.data > dist/sims-4-machines.txt
```

** NOTE **

In fact, there are not 4 machines in working. The only 3 machines(Slave) are working, but one of them is Master, so that is controlling others.
And you should know that 3 machines made results, so the results of 3 reducers are not sorted. Finally you can see the result having 3 sections.
