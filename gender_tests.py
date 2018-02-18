#This is a python program to perform a t-test and
#permutation test on a given csv file

## Import the packages
import numpy as np
from scipy import stats
from scipy.special import stdtr
import csv
#from decimal import Decimal

#import and read the height.csv file into a tuple list
with open('Heights.csv', 'rb') as f:
    reader = csv.reader(f)
    height_list = list(reader)

#Get Sample Size of Male
mList = [] #create an array to to hold the values
for height in height_list: #iterate through the tuple
    if height[1] != "" and height[1].isdigit(): #if the field is not blank
        mList.append(height[1]) #add the record to the array
Nm = len(mList) #do not count the header row

#Get Sample Size of Female
fList = [] #create an array to to hold the values
for height in height_list: #iterate through the tuple
    if height[0] != "" and height[0].isdigit(): #if the field is not blank
        fList.append(height[0]) #add the record to the array
Nf = len(fList) #do not count the header row

#Turn list of strings to numeric type.
a = np.array(mList).astype(np.float)
b = np.array(fList).astype(np.float)
print "Male List"
print "Size: " + str(len(mList))
print a
print "Female List"
print "Size: "+ str(len(fList))
print b
#
print "Perform t-test:"
#State the null and alternative hypothese
nH = "Null Hypothese: The height of men and women are the same."
aH = "Alternative Hypothese: The height of men and women are different"
print nH
print aH
# #Calculate the variance to get the standard deviation
var_a = a.var(ddof=1)
var_b = b.var(ddof=1)
print "variance of Male List is " + str(var_a)
print "Variance of Female List is " + str(var_b)

# Calculate the t-statistics
print("Calculated t-statistic and p-value")
print "The mean of the Male List is " + str(a.mean())
print "The mean of the Female List is " + str(b.mean())
tf = (a.mean() - b.mean()) / np.sqrt(var_a/Nm + var_b/Nf)
adof = Nm - 1
bdof = Nf - 1
dof = (var_a/Nm + var_b/Nf)**2 / (var_a**2/(Nm**2*adof) + var_b**2/(Nf**2*bdof))
print "The degrees of freedom for both list is " + str(dof)
pf = 2*stdtr(dof, -np.abs(tf))
#get the critical t-value
cTV = stats.t.cdf(tf,df=adof+bdof)
alpha = 0.05
print ("The critical t-value is " + str(cTV))
print("t-statistic1 = %g " % (tf))
print("p-value1 = " + str('{0:.5f}'.format(pf)))

# #Note that we multiply the p value by 2 because its a two tail t-test
#You can see that after comparing the t statistic with the critical t value
#(computed internally) we get a good p value of 0.00002 and thus we reject the null hypothesis
#and thus it proves that the mean of the two distributions are different and statistically significant.
#
print("Cross Checking with the internal scipy function...")
t2, p2 = stats.ttest_ind(a, b, equal_var=False)
print("t-statistic2 = %g " % (t2))
print("p-value2 = " + str('{0:.5f}'.format(p2)))
#To evaluate if your null hypothese is rejected or not, you can either
#1. Compare the critical t-value to the t-statistic
#if tf >= cTV:
#    print("Reject null hypothese. There are statistically significant differences between the two populations.")
#else:
#    print("Do not reject null hypothese. There is no statistically significant differences between the two populations.")
#2. Compare the p-value to the significance level (alpha)
if pf <= alpha:
    print("For t-test: Reject null hypothese. There are statistically significant differences between the two populations.")
else:
    print("For t-test: Do not reject null hypothese. There is no statistically significant differences between the two populations.")
print "Perform permutation test (Monte Carlo method)"
#a function to do a permuntation test on 2 arrays. The parm nmc is the number of permutations
def exact_mc_perm_test(xs, ys, nmc):
    n1,n2, k = len(xs),len(ys), 0
    #calculate the difference in mean between the 2 given samples
    tObs = np.abs(float(np.mean(xs)) - float(np.mean(ys)))
    zs = np.concatenate([xs, ys])
    #for the list of the given size
    for j in range(nmc):
        #create a list of random permutations
        np.random.shuffle(zs)
        #calculate and record the difference in sample means for each permutation
        m1 = float(np.mean(zs[:n1]))
        m2 = float(np.mean(zs[n2:]))
        tPmt = np.abs(float(m1 - m2))
        #calculate p-value as the proportion of sampled permutations where the difference
        #in mean was >= Tobs
        if tPmt >= tObs:
            k += 1
    return float(k/nmc)
pValue = exact_mc_perm_test(a, b, 1000)
print "p-value = " + str('{0:.4f}'.format(pValue))
#if p-value < significance level of 0.05, then reject the null hypothese that there is no sig. difference between the
#2 populations
alpha = 0.05
if pValue < alpha:
    print "For permutation test: Reject the null hypothese that there is no significant difference between the height of men and women"
else:
    print "For permutation test: Do not reject the null hypothese. There is no statsitcally significant difference between the height of men and women"
