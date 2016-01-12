from mrjob.job import MRJob

class SpendByCustomer(MRJob):

    def mapper(self, _, line):
        (customer, item, orderAmount) = line.split(',')
        yield customer, float(orderAmount)

    def reducer(self, customer, orders):
        yield customer, sum(orders)

if __name__ == '__main__':
    SpendByCustomer.run()
