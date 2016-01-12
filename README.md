# hadoop_python
This repository for udemy lecture; Taming Big Data with MapReduce and Hadoop

## Development
### Preparation
Use python(<=2.7.10) and MRJob library
* MRJob library install
```console
pip install mrjob
```

### Data
* [Movielens](http://grouplens.org/datasets/movielens/ "Movielens")

In this repository, we use ml-100k

```console
wget http://files.grouplens.org/datasets/movielens/ml-100k.zip
```

### Test
* Rating Counter of ml-100k data
```console
cd app
python RatingCounter.py ../data/ml-100k/u.data
```



