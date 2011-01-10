#blocktodo: this file should be deleted after testing is successful

from test_garlicsim.test_asynchronous_crunching.test_on_the_fly import tests

if __name__ == '__main__':
    for result in tests.test():
        check = result[0]
        args = result[1:]
        check(*args)