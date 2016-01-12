from mrjob.job import MRJob

class MRCustomerOrderAmount(MRJob):

    def mapper(self, _, line):
        (customer, itme, order_amount) = line.split(',')
        yield customer, float(order_amount)

    def reducer(self, customer, orders):
        yield customer, sum(orders)

if __name__ == '__main__':
    MRCustomerOrderAmount.run()
