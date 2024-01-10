import pandas
import csv
from keras.models import Sequential

from keras.layers import Dense
from scikeras.wrappers import KerasClassifier

from keras.utils import to_categorical, plot_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder

# load dataset
dataframe = pandas.read_csv("../../../data/Tags-en_uncertainity_handling_sample_dawn_20230925_1001-2.csv",
                            quoting=csv.QUOTE_MINIMAL,
                            sep=',',
                            header=0)

categorical_feature_columns = ["top_parse_parser_identifier",
                               "combined_dialogidentifier_cleaned",
                               "device_interface_id",
                               "device_power", "invocation_type",
                               "combined_speakeasy_category"]

float_feature_columns = [6, 7, 9]

dataset = dataframe.values
false_trigger_interactions = set()
asr_errors_interactions = set()
background_noise_interactions = set()

for r in dataset:
    if r[0].startswith("ASR Error"):
        asr_errors_interactions.add(r[1])
    elif r[0] == "Audio Quality - Background Noi":
        background_noise_interactions.add(r[1])
    elif r[0] == "False Trigger":
        false_trigger_interactions.add(r[1])

ask_to_repeat_interactions = asr_errors_interactions & background_noise_interactions

print(ask_to_repeat_interactions)

new_dataframe = pandas.read_csv("../../../data/Tags-en_uncertainity_handling_sample_dawn_20230925_1001-2.csv",
                                index_col="tag",
                                quoting=csv.QUOTE_MINIMAL,
                                sep=',',
                                header=0).drop_duplicates()
# X_float = dataset[:, float_feature_columns].astype(float)
X = pandas.get_dummies(new_dataframe,
                       dummy_na=False,
                       dtype=float,
                       columns=categorical_feature_columns).values

print(X)
print(len(X))
print(len(X[0]))
mitigateCount = 0
askToRepeatCount = 0
noOpCount = 0

Y = []
for d in X:
    if d[0] in false_trigger_interactions:
        Y.append("MitigateFalseTrigger")
        mitigateCount += 1
    elif d[0] in ask_to_repeat_interactions:
        Y.append("AskToRepeat")
        askToRepeatCount += 1
    else:
        Y.append("NoOp")
        noOpCount += 1

X = X[:, 1:]
print(X)
print(len(X))
print(len(X[0]))
print(mitigateCount)
print(askToRepeatCount)
print(noOpCount)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = to_categorical(encoded_Y)


# define baseline model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(128, input_dim=219, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    plot_model(model, show_shapes=True, show_layer_names=True, show_layer_activations=True,
               to_file='../../../data/my_model.png')
    return model


estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
