##
# A simple image signature knn example
#
# Author: Fabrício G. M. de Carvalho, Ph.D.
##


import matplotlib.py
def mode(v,key):
    '''
    :param v: k nearest neighbors
    :param key: attribute that stores the class
    :return: most frequent class
    '''
    classes_count = []
    classes = [] #most frequent classes
    for v_i in v:
        if v_i['class'] not in classes:
            classes.append(v_i['class'])

    for c in classes:
        classes_count.append({'class':c, 'count':0})
    for item in v:
        for c in range(len(classes_count)):
            if classes_count[c]['class'] == item[key]:
                classes_count[c]['count'] += 1
                break
    bubble_sort(classes_count, 'count')
    return classes_count[len(classes_count)-1]['class']


def knn(templates, unknown, k):
    """
    :param templates: List containing Labelled templates
    :param unknown: unclassified item
    :param k: number of nearest neighbors
    :return: the most frequent class
    """
    d_t_u = []
    classes = []
    for template in templates:
         d_t_u.append( {'class': template['class'],
                        'd': distance(template['feature_vector'], unknown['feature_vector'])})

    bubble_sort(d_t_u, 'd')
    print(d_t_u[:k])
    most_frequent_class = mode(d_t_u[:k],'class')
    return most_frequent_class

