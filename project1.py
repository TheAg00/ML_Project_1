import requests
import numpy as np
from scipy import stats


# Συνάρτηση που παίρνει τα δεδομένα από το API.
def getData():
    try:
        # Κάνουμε ένα GET request στο API.
        response = requests.get("http://127.0.0.1:5000/get_data")

        # Ελέγχουμε αν το request ήταν επιτυχές.
        if response.status_code == 200:
            print("Data received from API successfully!")

            # Επιστρέφουμε τα δεδομένα ως λίστα λεξικών.
            return response.json()

        print("Failed to receive data from API! Status code:", response.status_code)
    except Exception as e:
        print("Failed to receive data from API!")
        print("Error:", str(e))

class FilterEstates():
    def __init__(self, filteredOptions, realEstateData):
        self.realEstateData = realEstateData
        self.filteredOptions = filteredOptions

    def insertData(self):
        # Αρχικοποιούμε το λεξικό που θα βάλουμε τις τιμές που θα εισάγει ο χρήστης.
        insertedData = dict()

        # Δίνουμε το id του ακινήτου.
        insertedId = len(self.realEstateData)
        insertedData["id"] = insertedId

        # Ζητάμε από τον χρήστη να δώσει την περιοχή του ακινήτου.
        while True:
            print("Insert area(Madrid): ", end="")

            insertedArea = input()

            # Ελέγχουμε ώστε να μην έχουμε κενό string
            if insertedArea: break

            # Εμφανίζουμε σφάλμα αν ο χρήστης έδωσε κενή περιοχή και ξαναζητάμε εισαγωγή.
            print("Invalid Input!")

        insertedData["area"] = insertedArea + ", Madrid"

        # Τετραγωνικά μέτρα.
        while True:
            print("Insert square meters: ", end = "")
            try:
                insertedM2 = int(input())

                if insertedM2 > 0: break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")

        insertedData["m2"] = insertedM2

        # Αριθμό δωματίων.
        while True:
            print("Insert number of rooms: ", end = "")
            try:
                insertedRooms = int(input())
                if insertedRooms >= 0: break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        insertedData["n_rooms"] = insertedRooms
            
        # Διεύθυνση.
        while True:
            print("Insert address: ", end = "")
            insertedAddress = input()

            # Ελέγχουμε ώστε να μην έχουμε κενό string
            if insertedAddress: break

            print("Invalid Input!")


        insertedData["address"] = insertedAddress

        # Τιμή πώλησης.
        while True:
            print("Insert price: ", end = "")
            try:
                insertedPrice = int(input())

                if insertedPrice > 0: break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")

        insertedData["buy_price_2024"] = insertedPrice

        # Έτος κτήσης.
        while True:
            print("Insert build year: ", end = "")
            try:
                insertedBuildYear = int(input())

                if insertedBuildYear > 0: break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")

        insertedData["build_year"] = insertedBuildYear

        # Ζητάμε από τον χρήστη να μας πει αν το ακίνητο έχει πάρκιγκ.
        while True:
            print("Does the estate have a parking lot? (Y/n): ", end = "")
            insertedParking = input()

            if insertedParking == "y" or insertedParking == "Y":
                insertedData["parking"] = True
                break

            if insertedParking == "n" or insertedParking == "N":
                insertedData["parking"] = False
                break
            
            print("Invalid Input!")

        # Μεταφέρουμε τις πληροφορίες που εισήγαγε ο χρήστης στο τέλος των δεδομένων μας.
        self.realEstateData.append(insertedData)


    def areaFilter(self):
        avaliableAreas = list()
        interestedAreas = list()

        # Παίρνουμε όλες τις διαθέσιμες περιοχές από τα δεδομένα μας.
        for area in realEstateData:
            if area["area"] not in avaliableAreas: avaliableAreas.append(area["area"])


        while True:
            # Εμφανίζουμε όλες τις περιοχές για να επιλέξει ο χρήστης.
            print("Insert the area you are interested in:")
            i = 1
            for area in avaliableAreas:
                print(str(i) + ". " + area)
                i += 1

            # Ο χρήστης επιλέγει περιοχή με έλεγχο εγκυρώτητας.
            while True:
                try:
                    choice = int(input())
                    
                    if choice > 0 and choice < i + 1:
                        interestedAreas = avaliableAreas[choice - 1]
                        break
                    print("Invalid input!")
                except ValueError:
                    print("Invalid Input!")

            # Ρωτάμε τον χρήστη αν θέλει να επιλέξει και άλλη περιοχή.
            while True:
                print("Would you like to insert another area?(Y/n): ", end = "")
                choice = input()
                
                if choice == "n" or choice == "N":
                    # Αν δε θέλει, ενημερώνουμε το φίλτρο μας.
                    self.filteredOptions["area"] = interestedAreas
                    return
                if choice == "y" or choice == "Y": break
                print("Invalid Input!")


    def m2Filter(self):
        interestedM2 = list()

        # Ρωτάμε τον χρήστη τα ελάχιστα τετραγωνικά μέτρα που τον ενδιαφέρουν.
        while True:
            try:
                print("Insert the minimum square meters you are interested in: ", end = "")
                minM2 = float(input())
                if minM2 > 0: 
                    interestedM2.append(minM2)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ρωτάμε τον χρήστη τα μέγιστα τετραγωνικά μέτρα που τον ενδιαφέρουν.
        while True:
            try:
                print("Insert the maximum square meters you are interested in: ", end = "")
                maxM2 = float(input())
                if maxM2 >= minM2:
                    interestedM2.append(maxM2)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ενημερώνουμε το φίλτρο μας με τα τετραγωνικά μέτρα.
        self.filteredOptions["m2"] = interestedM2


    def roomsFilter(self):
        interestedRoomNum = list()

        # Ρωτάμε τον χρήστη τον ελάχιστο αριθμό δωματίων που τον ενδιαφέρουν.
        while True:
            try:
                print("Insert the minimum number of rooms you are interested in: ", end = "")
                minRooms = int(input())
                if minRooms >= 0: 
                    interestedRoomNum.append(minRooms)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ρωτάμε τον χρήστη το μέγιστο αριθμό δωματίων που τον ενδιαφέρουν.
        while True:
            try:
                print("Insert the maximum number of rooms you are interested in: ", end = "")
                maxRooms = int(input())
                if maxRooms >= minRooms:
                    interestedRoomNum.append(maxRooms)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ενημερώνουμε το φίλτρο μας με τον αριθμό δωματίων.
        self.filteredOptions["n_rooms"] = interestedRoomNum


    def priceFilter(self, realEstateData):
        interestedPrice = list()

        # Ρωτάμε τον χρήστη την ελάχιστη τιμή που τον ενδιαφέρει.
        while True:
            try:
                print("Insert the minimum price you are interested in:", end = "")
                minPrice = int(input())
                if minPrice > 0:
                    interestedPrice.append(minPrice)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ρωτάμε τον χρήστη τη μέγιστη τιμή που τον ενδιαφέρει.
        while True:
            try:
                print("Insert the maximum price you are interested in: ", end = "")
                maxPrice = int(input())
                if maxPrice >= minPrice:
                    interestedPrice.append(maxPrice)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ενημερώνουμε το φίλτρο μας με την τιμή.
        self.filteredOptions["price"] = interestedPrice


    def buildYearFilter(self):
        interestedBuildYear = list()
        
        # Ρωτάμε τον χρήστη το πόσο παλιό θέλει το ακίνητό του.
        while True:
            try:
                print("Insert the minimum build year you are interested in(Earliest avaliable build year:", end = "")
                minBuildYear = int(input())
                if minBuildYear >= 0: 
                    interestedBuildYear.append(minBuildYear)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ρωτάμε τον χρήστη το πόσο νέο θέλει το ακίνητό του.
        while True:
            try:
                print("Insert the maximum build year you are interested in(Latest avaliable build year:", end = "")
                maxBuildYear = int(input())
                if maxBuildYear >= minBuildYear:
                    interestedBuildYear.append(maxBuildYear)
                    break
                print("Invalid Input!")
            except(ValueError):
                print("Invalid Input!")
        
        # Ενημερώνουμε το φίλτρο μας.
        self.filteredOptions["build_year"] = interestedBuildYear
        


    def parkingFilter(self):
        # Ρωτάμε τον χρήστη αν το ακίνητό το θέλει να έχει παρκινγκ.
        while True:
            print("Would you like for the estate to have a parking?(Y/n): ", end = "")
            choice = input()
            if choice == "y" or choice == "Y":
                self.filteredOptions["has_parking"] = True
                return
                
            if choice == "n" or choice == "N":
                self.filteredOptions["has_parking"] = False
                return
            print("Invalid Input!")


    # Εφμανίζουμε μενού επιλογής για το φίλτρο, ώστε ο χρήστης να επιλέξει τα χαρακτηρηστικά που τον ενδιαφέρουν.
    def filterMenu(self):
        while True:
            print("Choose from the filter below which estate you're intrested in:")
            print("1. Area")
            print("2. Square meters")
            print("3. Number of rooms")
            print("4. Buy price")
            print("5. Build year")
            print("6. Has parking")
            print("7. Show results")

            try:
                choice = int(input("Insert choice: "))

                if choice >= 1 and choice <= 7: return choice
                print("Invalid input!")

            except ValueError:
                print("Invalid input!")


    def chooseFitler(self):

        while True:
            filterChoice = self.filterMenu()
            print()

            if filterChoice == 1: self.areaFilter()

            if filterChoice == 2: self.m2Filter()

            if filterChoice == 3: self.roomsFilter()

            if filterChoice == 4: self.priceFilter()

            if filterChoice == 5: self.buildYearFilter()

            if filterChoice == 6: self.parkingFilter()

            if filterChoice == 7: return

            while True:
                print("Would you like to choose another filter?(Y/n): ", end = "")
                choice = input()

                if choice == "n" or choice == "N": return
                if choice == "y" or choice == "Y": break
                print("Invalid Input!")


class PredictEstatePrice(FilterEstates):
    def __init__(self):
        self.y = np.array([2021, 2022, 2023, 2024])

    def predictionEquation(slope, x, intercept):
        return int(intercept + slope * x) # y = β0 + β1 * x

    def predictPrice(interestedEstates):
        for estate in interestedEstates:
            x = np.array([estate["buy_price_2021"], estate["buy_price_2022"], estate["buy_price_2023"], estate["buy_price_2024"]])

            slope, intercept, r, p, std_err = stats.linregress(y, x)

            price2025 = predictionEquation(slope, 2025, intercept)

            print("For estate with address " + estate["address"] + ", and id " + str(estate["id"]) + ":")
            print("Buy price 2021:", estate["buy_price_2021"])
            print("Buy price 2022:", estate["buy_price_2022"])
            print("Buy price 2023:", estate["buy_price_2023"])
            print("Buy price 2024:", estate["buy_price_2024"])
            print("Predicted price for 2025:", price2025)
            print()


    def printPrices(self):
        filterKeys = list(filter.keys())
        totalKeys = len(filterKeys)

        # Αν ο χρήστης επέλεξε φίλτρα, ελέγχουμε τα ακίνητα που ταυτίζουν με αυτά. Αλλιώς εμφανίζουμε τις προβλέψεις για όλα τα ακίνητα.
        if totalKeys > 0:
            interestedEstates = list()
            
            # Για κάθε ακίνητο, ελέγχουμε αν ισχύουν τα φίλτρα που επέλεξε ο χρήστης.
            for estate in realEstateData:
                keysCount = 0
                for key in filterKeys:
                    # Αν η τιμή του φίλτρου ταυτίζεται με την τιμή που έχουμε στα δεδομένα, αυξάνουμε τον μετρητή.
                    if filter[key] == estate[key]: keysCount += 1

                # Αν ο μετρητής είναι ίσος με τον αριθμό των φίλτρων που επέλεξε ο χρήστης, τότε το ακίνητο ταιριάζει με τις προτημήσεις του χρήστη.
                if keysCount == totalKeys:
                    interestedEstates.append(estate)

            predictPrice(interestedEstates)
            return

        predictPrice(realEstateData)

    
    def showResults(self):
        printPrices()

    def showPredictions(self):
        self.chooseFitler()
        self.showResults()





    

if __name__ == "__main__":
    # Παίρνουμε τα δεδομένα από το API σε μορφή λίστας.
    realEstateData = getData()

    filteredOptions = dict()
    filter = FilterEstates(filteredOptions, realEstateData)

    # Εμφανίζουμε μήνυμα υποδοχής του χρήστη και του δίνουμε μενού επιλογών.
    print("Welcome!")
    while True:
        print("Select an option:")
        print("1. Insert data")
        print("2. Show future price predictions")
        print("3. Exit")

        # Έλεγχος εγκυρώτητας.
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1: filter.insertData()
            if choice == 2: showPredictions()
            if choice == 3: break
        except ValueError:
            print("Invalid input!")
    
    print("Exitting...")

