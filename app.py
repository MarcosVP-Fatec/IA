from kmeans import KMeans
from matplotlib import pyplot as plt


kmeans = KMeans(2)
feature_vectors = [ [1, 1, 0],
                    [1, 1, 0],
                    [0, 0, 1],
                    [0, 0, 1],
                    [1, 1, 1],
                    [1, 1, 0] ]
kmeans.init_centers(feature_vectors)
kmeans.classify_vectors()
print('Initial centers: ')
print(kmeans.centers)
center_i = [] #used to plot center coordinate evolution
center_i.append(kmeans.centers[0])
center_j = [] #used to plot center coordinate evolution
center_j.append(kmeans.centers[1])
print('Initialy classified vectors: ')
print(kmeans.classified_vectors)
for i in range(10): #Number of iterations as stoping criterion
    kmeans.classify_vectors()
    kmeans.calc_centers()
    center_i.append(kmeans.centers[0])
    center_j.append(kmeans.centers[1])
print('Final centers: ')
print(kmeans.centers)
print('Final classified vectors ')
print(kmeans.classified_vectors)

n_pos_center = 0
for temp_center in [center_i, center_j]:
    plt.title("Center " + str(n_pos_center))
    plt.plot(temp_center)
    plt.legend(['ci1', 'ci2', 'ci3'])
    plt.show()
    n_pos_center += 1

