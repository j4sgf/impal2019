import multiprocessing as mp

from multiprocessing import Pool


def square(x):
    # calculate the square of the value of x
    return x * x


if __name__ == '__main__':
    print("Number of processors: ", mp.cpu_count())
    from time import time
    start_time = time()
    # Define the dataset
    dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    result = []
    # Output the dataset
    print('Dataset: ' + str(dataset))
    # for a in dataset:
    #     result.append(square(a))
    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    agents = 4
    chunksize = 1
    with Pool(processes=agents) as pool:
        result = pool.map(square, dataset, chunksize)

    # Output the result
    end_time = time()
    print('Result:  ' + str(result))
    print("Total prediction time : {0}".format(end_time - start_time))
