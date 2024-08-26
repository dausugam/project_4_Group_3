import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Load the dataset
file_path = 'Sleep_health_and_lifestyle_dataset.csv'
df = pd.read_csv(file_path)

df.drop('Person ID', axis=1, inplace=True)


df['Systolic'] = df['Blood Pressure'].apply(lambda x: int(x.split('/')[0]))
df['Diastolic'] = df['Blood Pressure'].apply(lambda x: int(x.split('/')[1]))
df.drop('Blood Pressure', axis=1, inplace=True)

categorical_columns = ['Gender', 'Occupation', 'BMI Category']
df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

df['Sleep Disorder'] = df['Sleep Disorder'].map({'None': 0, 'Insomnia': 1, 'Sleep Apnea': 2})

df['Sleep Disorder'] = df['Sleep Disorder'].fillna(0)

print(df['Sleep Disorder'].unique())

numerical_columns = ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Stress Level', 'Heart Rate', 'Daily Steps', 'Systolic', 'Diastolic']

scaler = StandardScaler()

df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

X = df.drop('Sleep Disorder', axis=1)  
y = df['Sleep Disorder']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

