import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

def main():
    output_dir = "../output/model_result"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    df = pd.read_csv("../output/input_kosis/전국_기상.csv")

    df['rainfall_sum'] = df.filter(regex='rainfall').sum(axis='columns')
    df['sunshine_sum'] = df.filter(regex='sunshine').sum(axis='columns')

    y = df['value']
    X = df[['cumsum_tavg', 'rainfall_sum', 'sunshine_sum']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_predict = model.predict(X_test)
    print(y_predict)
    print(model.score(X_test, y_test))

    mae = mean_absolute_error(y_predict, y_test)
    r2 = r2_score(y_predict, y_test)

    plt.scatter(y_test, y_predict)
    plt.scatter(y_train, model.predict(X_train))
    plt.plot([0, max(y_predict)], [0, max(y_predict)])
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"Linear Regression | mae: {mae:.4f} | r2: {r2:.4f}")

    # plt.show()
    plt.savefig(os.path.join(output_dir, "linear_regression_all.png"))

    # print(["{}: {}".format(x, y) for x, y in zip(X.columns, model.coef_)])

if __name__ == '__main__':
    main()