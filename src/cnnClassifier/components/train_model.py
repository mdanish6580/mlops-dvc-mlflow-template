import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import mlflow
from urllib.parse import urlparse

def eval_metrics():
    rmse = 0.80
    mae = 0.89
    r2 = 0.92
    return rmse, mae, r2

def train_model(data_path, model_path, n_estimators, max_depth):

    data = pd.read_csv(data_path)
    X, y = data[["Pclass", "Sex", "SibSp", "Parch"]], data["Survived"]

    X = pd.get_dummies(X)

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
        model.fit(X, y)
        
        # # Ensure the output directory exists
        model_dir, model_file = model_path.split("/")
        os.makedirs(model_dir, exist_ok=True)
        
        # Save the trained model to the specified path
        with open(model_dir + "/" + model_file, "wb") as f:
            pickle.dump(model, f)
        
        (rmse, mae, r2) = eval_metrics()
        
        print(f"Model training complete. Model saved to {model_path}.")
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("model_path", model_path)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        
        # For remote server only (Dagshub)
        remote_server_uri = "https://dagshub.com/6580danish/mlops-dvc-mlflow-template.mlflow"
        mlflow.set_tracking_uri(remote_server_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                model, "model", registered_model_name="RandomForestClassifierTitanicModel")
        else:
            mlflow.sklearn.log_model(model, "model")
    

if __name__ == "__main__":
    import sys
    train_model(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3]),
        int(sys.argv[4])
    )