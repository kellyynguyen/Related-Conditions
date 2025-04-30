import csv
import queue
from collections import deque
import random
random.seed(17)

class ConditionPredictor:
    """
    A node in linked list.

    Attributes
    ----------
    symptomWeights: dict
        A dictionary that stores the weights of symptoms.

    conditionSymptoms: dict
        A dictionary that stores the symptoms associated with each condition.

    adjList: dict
        A dictionary that represents the adjacency list of the condition graph.

    loadSymptomWeights: function
        A function that loads the symptom weights from a CSV file.

    generateAdjList: function
        A function that generates the adjacency list from a CSV file.

    getPath: function
        A function that finds the path between two conditions.

    getCondition: function
        A function that retrieves the condition based on a list of symptoms.

    Parameters
    ----------
    fileCondtion: str
        The name of the file containing condition data.

    fileWeights: str
        The name of the file containing symptom weights.
    """

    def __init__(self, fileCondition, fileWeights) -> None:
        """
        Constructs all the necessary attributes for the ConditionPredictor object.

        Parameters
        ----------
        fileCondition: str
            The name of the file containing the condition and associating symptom data.

        fileWeights: str
            The name of the file containing the symptom weights.
        """

        self.symptomWeights = {}
        self.conditionSymptoms = {}
        self.adjList = {}
        self.loadSymptomWeights(fileWeights)
        self.generateAdjList(fileCondition)

    def loadSymptomWeights(self, fileName):
        """
        Reads a file and loads the symptom weights into a dictionary.

        Parameters
        ----------
        fileName: str
            The name of the file to read the data from.

        Attributes
        ----------
        symptomWeights : dict
            A dictionary that stores the weights of symptoms.

        Returns
        -------
        None
        """

        with open(fileName, 'r', encoding="ISO-8859-1") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                symptom = row[0].strip().lower()
                weight = int(row[1])
                self.symptomWeights[symptom] = weight

    def generateAdjList(self, fileName) -> None:
        """
        Reads a file and builds an adjacency list representing condition connections.

        Parameters
        ----------
        fileName : str
            The name of the file to read the data from.

        Attributes
        ----------
        adjList : dict of dict/dict of list/ dict of tuple/etc...
        The key of the adjList is the name of the condition, and the value is a dictionary

        Returns
        -------
        None
        """

        with open(fileName, "r", encoding="ISO-8859-1") as file:
            reader = csv.reader(file)
            for row in reader:
                condition = row[0].strip().lower()
                symptoms = []
                for symptom in row[1:]:
                    symptom = symptom.strip().lower()
                    if symptom:
                        symptoms.append(symptom)
                self.conditionSymptoms[condition] = symptoms

        for condition1, symptoms1 in self.conditionSymptoms.items():
            for condition2, symptoms2 in self.conditionSymptoms.items():
                same_symptoms = []
                for symptom in symptoms1:
                    if symptom in symptoms2:
                        same_symptoms.append(symptom)
                    if same_symptoms:
                        totweight = 0
                        for symptom in same_symptoms:
                            weight = self.symptomWeights.get(symptom, 0)
                            totweight += weight
                        if condition1 not in self.adjList:
                            self.adjList[condition1] = {}
                        if condition2 not in self.adjList:
                            self.adjList[condition2] = {}
                        self.adjList[condition1][condition2] = totweight
                        self.adjList[condition2][condition1] = totweight

    def getPath(self, startCondition, endCondition):
        """
        Reads a file and builds an adjacency list representing condition connections.

        Parameters
        ----------
        fileName : str
            The name of the file to read the data from.

        Attributes
        ----------
        adjList : dict of dict/dict of list/ dict of tuple/etc...
        The key of the adjList is the name of the condition, and the value is a dictionary

        Returns
        -------
        [-1, []] if no path is found
        """

        if startCondition not in self.adjList or endCondition not in self.adjList:
            return [-1, []]

        if startCondition == endCondition:
            return [0, [startCondition]]

        visited = set()
        queue = deque()
        queue.append((startCondition, [startCondition]))
        visited.add(startCondition)

        while queue:
            condition, path = queue.popleft()
            for item in self.adjList[condition]:
                if item not in visited:
                    visited.add(item)
                    new_path = path + [item]
                    if item == endCondition:
                        return [(len(new_path)-1), new_path]

                    queue.append((item, new_path))

        return [-1, []]

    def getCondition(self, path) -> None:
        """
        Retrieve the condition based on the list of input symptoms.

        Parameters
        ----------
        path: list
            A list of symptoms representing the path between two conditions.

        Returns
        -------
        path: Any
            The route of conditions between the two inputs.
        """

        for i in range(len(path) - 1):
            condition1 = path[i]
            condition2 = path[i + 1]
            weight = self.adjList[condition1][condition2]
            print(f"Condition: {condition1} -> {condition2}, Severity of condition (total weight): {weight}")

    def getRelatedConditions(self, input_symptoms):
        """
        Gets related conditions based off an input of symptoms (str).

        Parameters
        ----------
        input_symptoms: str
            Symptoms user wants to explore.

        Returns
        -------
        Any
        """

        find_symptom = input_symptoms.split(",")
        for i in range(len(find_symptom)):
            find_symptom[i] = find_symptom[i].strip().lower()
        conditions = []

        for condition, symptoms in self.conditionSymptoms.items():
            for symptom in find_symptom:
                if symptom in symptoms:
                    conditions.append(condition)

        if conditions:
            print(f"{find_symptom} are/is a symptom(s) of: {conditions}")
        else:
            print(f"No conditions found that include the symptom(s) {find_symptom}.")

    def conditionList(self):
        """
        Returns a list of all conditions in the adjacency list.

        Parameters
        ----------
        fileName: str
            A file contianing conditions and symptoms.

        Returns
        -------
        None
        """

        list_conditon = list(self.adjList.keys())
        for condition in list_conditon:
            print(condition.title())

    def symptomsList(self):
        """
        A list of all symptoms in the adjacency list.

        Parameters
        ----------
        fileName: str
            A file contianing conditions and symptoms.

        Returns
        -------
        None
        """

        list_symptoms = []
        for symptom in self.symptomWeights.keys():
            list_symptoms.append(symptom)
        for symptom in list_symptoms:
            print(symptom.title())

def main():
    data = ConditionPredictor(fileCondition="dataset.csv", fileWeights="Symptom-severity.csv")

    print("Welcome to the Condtion Predictor!")
    print("This program predicts the path between two conditions based on symptoms.")
    print("Do you want to explore how two conditions are related? (yes/no)")
    explore_ans = input("Answer: ").strip().lower()

    while explore_ans:
        if explore_ans == "yes":
            data.conditionList()
            print("Please enter the names of two conditions to find the path between them.")

            start = input("First condition: ").strip().lower()
            end = input("Second condtion: ").strip().lower()

            steps, path = data.getPath(start, end)
            if steps == -1:
                print("No path found.")
            else:
                print(f"Steps from {start} to {end}: {steps}")
                data.getCondition(path)
            print("Do you want to explore how two conditions are related? (yes/no)")
            explore_ans = input("Answer: ").strip().lower()
            continue

        print("Do you want to search for a condition based on symptoms? (yes/no)")
        search = input("Answer: ").strip().lower()

        if search == "yes":
            data.symptomsList()
            print("Please enter symptoms to find condition(s).")
            condition = input("Symtpoms: ").strip().lower()
            print(data.getRelatedConditions(condition))
        else:
            break


if __name__ == '__main__':
    main()
