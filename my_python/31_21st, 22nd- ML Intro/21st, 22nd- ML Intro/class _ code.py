import numpy as np 	#Array		
import matplotlib.pyplot as plt		
import pandas as pd	

dataset = pd.read_csv(r"C:\Users\Admin\Desktop\NIT\1. NIT_Batches\1. MORNING BATCH\N_Batch -- 9AM _ SEP25\3. Dec\13th, 15th - ML\5. Data preprocessing\Data.csv")

x = dataset.iloc[:, :-1].values	
# DEPENDENT VARIABLE
y = dataset.iloc[:,3].values 

from sklearn.impute import SimpleImputer
imputer = SimpleImputer() 

imputer = imputer.fit(x[:,1:3]) 
x[:, 1:3] = imputer.transform(x[:,1:3]) 

from sklearn.preprocessing import LabelEncoder
labelencoder_x = LabelEncoder()
x[:,0] = labelencoder_x.fit_transform(x[:,0]) 

labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)

from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=0)
















