import json
import os
import pickle

import pandas as pd
import pika
from models import SelectedModel, SessionLocal, StatusEnum
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["RABBIT_URL"]))

channel = connection.channel()

channel.queue_declare(queue="training")


def prepare_data(file_path: str, prediction_field: str):
    X = pd.read_csv("../" + file_path)
    X = X.select_dtypes(["number", "bool"])
    y = X[prediction_field]
    X = X.drop(prediction_field, axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
    return X_train, X_test, y_train, y_test


def callback(ch, method, properties, body):
    print("consumed in trainer")
    config = json.loads(body)

    X_train, X_test, y_train, y_test = prepare_data(config["file_path"], config["prediction_field"])

    db = SessionLocal()

    if config["name"] == "LinearRegression":
        print("Training linear regression")

        model = LinearRegression(
            fit_intercept=config["params"]["fit_intercept"], positive=config["params"]["positive"]
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        evaluations = {
            "mae": mean_absolute_error(y_test, y_pred),
            "mse": mean_squared_error(y_test, y_pred),
        }

        db_model = db.query(SelectedModel).get(config["model_id"])
        db_model.evaluation = json.dumps(evaluations)
        db_model.status = StatusEnum.TRAINED

        db.commit()

        with open(f"../trained_models/{config['name']}{config['model_id']}.pkl", "wb") as pkl:
            pickle.dump(model, pkl)

    elif config["name"] == "LogisticRegression":
        # matrix = confusion_matrix(y_test, y_pred)
        print("Training random logistic regression")
    elif config["name"] == "RandomForestRegressor":
        print("Training random forest regressor")
    elif config["name"] == "RandomForestClassifier":
        print("Training random forest classifier model")
    else:
        print("Unknown model...")


channel.basic_consume(queue="training", on_message_callback=callback, auto_ack=True)

print("Started Consuming...")

channel.start_consuming()

channel.close()
