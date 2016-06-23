from munkres import Munkres
import sys
import copy

def replaced(array, u1, u2, cor):
	#copy array for isolation
	#Need to use deepcopy because of the nature of Python for treating 
	replaced = copy.deepcopy(array)
	#cor is the corresponding list
	for row, col in cor:
		#u1[row] and u2[col] is corresponded
		for idx in range(len(array)):
			#if the element of array is equal to u2[col]
			if array[idx] == u2[col]:
				#the element is corresponding to u1[row]
				#so isolated list replaced is replaced by u1[row]
				replaced[idx] = u1[row]
	return replaced

def benefit_to_cost(matrix):
	cost_matrix = []
	for row in matrix:
		cost_row = []
		for col in row:
			cost_row = cost_row + [(sys.maxsize - col)]
		cost_matrix = cost_matrix + [cost_row]
	return cost_matrix

def relabel(array1, array2):
	#this function returns relabeled array2

	if len(array1)==len(array2):
		# set1 is the unique set of array1
		set1 = set(array1)
		# u1 is the unique list of array1
		u1 = list(set1)

		# set2 is the unique set of array2
		set2 = set(array2)
		# set2 is the unique list of array1
		u2 = list(set2)
		
		#matrix is the Corresponding matrix between u1 and u2
		matrix = [[0 for i in range(len(u2))]for j in range(len(u1))]	

		for i in range(len(array1)):
			#item_1 is the index of array1's element in u1
			item_1 = u1.index(array1[i])
			#item_2 is the index of array2's element in u2
			item_2 = u2.index(array2[i])

			#this situation means 1 correspondence between item_1 and item2 is observed
			#so corresponding location in corresponding matrix is incremented
			matrix[item_1][item_2] = matrix[item_1][item_2] + 1

		cost_matrix = benefit_to_cost(matrix)

		#Munkers library solve the cost minimization problem
		#but I would like to solve benefit maximization problem
		#so convert benefit matrix into cost matrix

		#create mukres object
		m = Munkres()
		#get the most corresponded correspondance
		indexes = m.compute(cost_matrix)
		
		#I use array2 as Integer array so, convert it in case
    	array2 = map(int, array2)
    	
    	#call replaced function to relace array2 according to object indexes
    	replaced_matrix = replaced(array2, u1, u2, indexes)

    	return replaced_matrix

def relabel_cluster(clusters):
	#use first object in list object clusters as criteria
	criteria = clusters[0]

	# M is the number of review in each clustering
	M = len(criteria)
	
	# N is the number of clustering
	N = len(clusters)
	
	for idx in range(1,N):
		#if wrong size of clustering appears, stop the process
		if len(clusters[idx]) != M:
			print "Cluster "+str(idx)+" is out of size"
			return -1
		clusters[idx] = relabel(criteria, clusters[idx])
	return clusters

def transpose(array):
	#Transpose list
	return list(map(list, zip(*array)))

def voting(clusters):
	#Transpose Clusters
	clusters = transpose(clusters)
	voted = []
	for row in clusters:
		#Unique Set of item in the row
		u = list(set(row))
		#Counter corresponding to object u
		counter = [0 for i in u]
		
		# fill object counter by counting the object u in object row 
		for idx in range(len(u)):
			counter[idx] = row.count(u[idx])

		#find the index of the most appeared object in the row
		max_idx = counter.index(max(counter))

		#choose the most appeared object
		voted = voted + [u[max_idx]]
	
	#return the result of majority vote	
	return voted

if __name__ == '__main__':
	clusters = [[1,2,3,3,2,2,1], [3,2,1,1,1,1,4],[2,3,1,1,1,1,1]]
	print "Input:"
	for cluster in clusters:
		print cluster
	print "========"
	#relabeling Phase
	relabeled_clusters = relabel_cluster(clusters)
	print "relabeled clusters:"
	for cluster in clusters:
		print cluster
	print "========"

	#voting Phase
	print "Output:"
	print voting(relabeled_clusters)
	#print replace_by_cor([0,1,2],[[0,2],[1,1],[2,0]])