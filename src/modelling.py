from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score
)


def train_random_forest(
    X_train,
    y_train,
    X_eval,
    y_eval,
    n_estimators=100
):

    model = (
        RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42
        )
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_eval
    )

    accuracy = (
        accuracy_score(
            y_eval,
            predictions
        )
    )

    return (
        model,
        accuracy
    )


def train_svm(
    X_train,
    y_train,
    X_eval,
    y_eval
):

    model = SVC()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_eval
    )

    accuracy = (
        accuracy_score(
            y_eval,
            predictions
        )
    )

    return (
        model,
        accuracy
    )