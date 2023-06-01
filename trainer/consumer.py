import json
import pickle

import pandas as pd
import pika
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

channel = connection.channel()

channel.queue_declare(queue="training")


def callback(ch, method, properties, body):
    print("consumed in trainer")
    config = json.loads(body)

    X = pd.read_csv(f"upload/data/ready/{config.filename}")
    y = X[config["prediction_field"]]
    X = X.drop(config["prediction_field"], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

    if config["model"] == "LinearRegression":
        print("train linear regression")
        from sklearn.linear_model import LinearRegression

        model = LinearRegression(fit_intercept=config["fit_intercept"], positive=config["positive"])
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        matrix = confusion_matrix(y_test, y_pred)
        print(matrix)
        with open("trained_models/model.pkl", "wb") as pkl:
            pickle.dump(model, pkl)
    elif config["model"] == "RandomForestRegressor":
        print("train random forest regressor")
    elif config["model"] == "RandomForestClassifier":
        print("train random forest classifier model")
    else:
        print("Unknown model...")


channel.basic_consume(queue="training", on_message_callback=callback, auto_ack=True)

print("Started Consuming...")

channel.start_consuming()

channel.close()
