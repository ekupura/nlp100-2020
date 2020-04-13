import fire
import csv
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
csv.field_size_limit(1000000000)

class Main():
    def __init__(self):
        pass

    def a50(self):
        x, y = [], []
        with open('./NewsAggregatorDataset/newsCorpora.csv') as f:
            reader = csv.reader(f, delimiter="\t")
            articles = [row for row in reader]
            target = ["Reuters", "Huffington Post", "Businessweek", "Contactmusic.com", "Daily Mail"]
            for a in articles:
                if a[3] in target:
                    x.append(a[1])
                    y.append(a[4])
        x_train, x_tmp, y_train, y_tmp = train_test_split(x, y, test_size=0.2, random_state=0)
        x_test, x_valid, y_test, y_valid = train_test_split(x_tmp, y_tmp, test_size=0.5, random_state=0)

        def dump_dataset(_x, _y, filename):
            with open(filename, 'w') as _f:
                writer = csv.writer(_f, delimiter='\t')
                for _a, _b in zip(_x, _y):
                    writer.writerow([_a, _b])

        dump_dataset(x_train, y_train, "train.txt")
        dump_dataset(x_valid, y_valid, "valid.txt")
        dump_dataset(x_test, y_test, "test.txt")

    def a51(self):
        vectorizer = TfidfVectorizer()
        labelencoder = LabelEncoder()

        def text_reader(filename):
            with open(filename) as f:
                x, y = [], []
                reader = csv.reader(f, delimiter="\t")
                for row in reader:
                    x.append(row[0])
                    y.append(row[1])
                return x, y

        x_train_text, y_train_text = text_reader("./train.txt")
        x_valid_text, y_valid_text = text_reader("./valid.txt")
        x_test_text, y_test_text = text_reader("./test.txt")
        x_train = vectorizer.fit_transform(x_train_text).toarray()
        x_valid, x_test = vectorizer.transform(x_valid_text).toarray(), vectorizer.transform(x_test_text).toarray()
        y_train = labelencoder.fit_transform(y_train_text)
        y_valid, y_test = labelencoder.transform(y_valid_text), labelencoder.transform(y_test_text)

        def dataset_writer(_x, _y, filename):
            with open(filename, "w") as f:
                writer = csv.writer(f, delimiter=" ")
                for _a, _b in zip(_x, _y):
                    writer.writerow([list(_a), _b])

        dataset_writer(x_train, y_train, "train.feature.txt")
        dataset_writer(x_valid, y_valid, "valid.feature.txt")
        dataset_writer(x_test, y_test, "test.feature.txt")

        return x_train, x_valid, x_test, y_train, y_valid, y_test

    def a52(self):
        x_train, x_valid, x_test, y_train, y_valid, y_test = self.a51()
        classifier = LogisticRegression(random_state=0)
        classifier.fit(x_train, y_train)
        return classifier

    def a53(self):
        x_train, x_valid, x_test, y_train, y_valid, y_test = self.a51()
        classifier = self.a52()
        print(classifier.predict(x_test)[:20])
        print(classifier.predict_proba(x_test)[:20])

    def a54(self):
        x_train, x_valid, x_test, y_train, y_valid, y_test = self.a51()
        classifier = self.a52()
        print("accuracy={}".format(classifier.score(x_test, y_test)))

    def a55(self):
        x_train, x_valid, x_test, y_train, y_valid, y_test = self.a51()
        classifier = self.a52()
        y_train_pred = classifier.predict(x_train)
        y_test_pred = classifier.predict(x_test)
        print("train:")
        print(confusion_matrix(y_train, y_train_pred))
        print("test:")
        print(confusion_matrix(y_test, y_test_pred))

    def a56(self):
        x_train, x_valid, x_test, y_train, y_valid, y_test = self.a51()
        classifier = self.a52()
        y_train_pred = classifier.predict(x_train)
        y_test_pred = classifier.predict(x_test)
        print("train:")
        print("precision:{}".format(precision_score(y_train, y_train_pred)))
        print("recall:{}".format(recall_score(y_train, y_train_pred)))
        print(f1_score(y_train, y_train_pred))
        print("test:")
        print(precision_score(y_test, y_test_pred))
        print(recall_score(y_test, y_test_pred))
        print(f1_score(y_test, y_test_pred))

if __name__ == '__main__':
    fire.Fire(Main)
