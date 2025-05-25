import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    types = {
        "Administrative": int,
        "Administrative_Duration": float,
        "Informational": int,
        "Informational_Duration": float,
        "ProductRelated": int,
        "ProductRelated_Duration": float,
        "BounceRates": float,
        "ExitRates": float,
        "PageValues": float,
        "SpecialDay": float,
        "Month": {  # string to int
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "Apr": 3,
            "May": 4,
            "June": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11
        },
        "OperatingSystems": int,
        "Browser": int,
        "Region": int,
        "TrafficType": int,
        "VisitorType": {    # string to int
            "New_Visitor": 0,
            "Other": 0,
            "Returning_Visitor": 1
        },
        "Weekend": {    # string to int
            "FALSE": 0,
            "TRUE": 1
        },
        "Revenue": {    # string to int
            "FALSE": 0,
            "TRUE": 1
        }
    }

    # Read CSV file into dictionary
    with open(filename) as f:
        reader = csv.DictReader(f)

        for row in reader:
            data = []
            for column in row:
                if column in {"Month", "VisitorType", "Weekend"}:
                    # string to int
                    data.append(types[column][row[column]])
                elif column == "Revenue":
                    labels.append(types[column][row[column]])
                else:
                    # apply data types
                    data.append(types[column](row[column]))
            evidence.append(data)

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tp = 0 # true positive
    fp = 0 # false positive
    tn = 0 # true negative
    fn = 0 # false negative
    for label, predicted in zip(labels, predictions):
        if label == 1 and predicted == 1:
            tp += 1 

        if label == 0 and predicted == 1:
            fn += 1 

        if label == 0 and predicted == 0:
            tn += 1 
        
        if label == 1 and predicted == 0:
            fp += 1 

    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
