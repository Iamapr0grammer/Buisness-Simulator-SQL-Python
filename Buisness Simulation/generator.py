import random, data
from datetime import date
from dateutil.relativedelta import relativedelta


# DATA

restaurant_reputation = 10


# list of male names
male_names = [
    # Standard Male Names
    "Adam", "Ben", "Carl", "David", "Ethan", "Frank", "George", "Henry",
    "Ian", "Jack", "Kyle", "Luke", "Mark", "Nathan", "Oliver", "Paul",
    "Quentin", "Ryan", "Steve", "Tom", "Victor", "William", "Xavier", "Yanni", "Zach",
    
    # Nerd-Approved Names
    "Alan", "Dennis", "Guido", "Linus", "Elon", "Bill", "Steve",
    "Richard", "Tim", "Bjarne",
    
    # version 2
    "Greg", "Todd", "Chuck", "Barry",
    "Neil", "Phil", "Craig",
    "Randy", "Doug", "Frank",
    
    # Overkill Names
    "Maximus", "Thorvald", "Magnus", "Apollo", "Xerxes", "Leonardo",
    "Hannibal", "Atticus", "Titan", "Zephyr"
]

# list of female names
female_names = [
    # Standard Female Names
    "Alice", "Beth", "Clara", "Diana", "Emma", "Fiona", "Grace", "Hannah",
    "Isla", "Jane", "Katie", "Luna", "Maria", "Nina", "Olivia", "Penny",
    "Queenie", "Rachel", "Sarah", "Tina", "Uma", "Vera", "Wendy", "Xena", "Yara", "Zoe",
    
    # Nerd-Approved Names
    "Ada",       
    "Grace",     
    "Radia",     
    "Margaret",  
    "Joan",      
    "Barbara",   
    "Karen",    
    "Frances",  
    "Marissa",   
    "Shafi",     

    # version 2
    "Sally", "Tina", "Claire", "Bonnie",
    "Nina", "Faye", "Cassie",
    "Rita", "Deb", "Wanda",

    # Overkill Names
    "Athena", "Freya", "Seraphina", "Bellatrix", "Juno", "Andromeda",
    "Lilith", "Electra", "Valkyrie", "Nova"
]


# list of family names
family_names = [
    # Common and Classic
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",

    # Nerd-Approved Surnames
    "Turing",       
    "Hopper",       
    "Lovelace",     
    "Hamilton",     
    "Knuth",        
    "Liskov",       
    "Torvalds",     
    "Dijkstra",     
    "Berners-Lee",  
    "Spärck Jones", 

    # Fictionally Spicy
    "Skywalker", "Kenobi", "Stark", "Wayne", "Potter", "Malfoy", "Snape",
    "Romanoff", "Banner", "Holmes", "Moriarty", "Riker", "Picard", "Ripley", "Kirk",

    # Unnecessarily Cool
    "Ravenwood", "Storm", "Blackthorn", "Graves", "Nightshade", "Blaze",
    "Ashcroft", "Thorne", "Hawke", "Crimson"
]



def generate_person():
    sex = random.randint(1,2)
    if sex == 1:
        sex = "male"
    else:
        sex = "female"
    
    name = ""

    if sex == "male":
        name = random.choice(male_names)
    else:
        name = random.choice(female_names)

    family_name = random.choice(family_names)

    age = random.randint(18,100)

    dish = random.choice(data.dish_full_list)

    person = [name, family_name, dish, age, sex]

    return person



def generate_random_expanses(day):
    change_for_random_expanse = 0

    starting_day = day

    for i in range(30):
        starting_day = starting_day + relativedelta(day=1)

        change_for_random_expanse += random.randint(1,5)

        if change_for_random_expanse > 20:
            money_change = random.randint(-10000, 10000)
            reason = "Casino Trip"
            data.money_change(money_change, reason, day, "Casino")
            change_for_random_expanse = 0 # reset the chance



def full_month_clients():
    global restaurant_reputation

    print(restaurant_reputation)

    gained_money = 0 # for now it will be 100, later I will create a reputation system, that can be damaged or reapaired
    staff = data.get_staff()

    working_staff = []
    staff_power = 3 # you as the owner can also serve the customers, this 3 represents the owner

    for employee in staff:
        if employee[11] == "working": # if working status "working"
            working_staff.append(employee)  
            staff_power += 2 + (employee[9] // 3) # 5 basic + 0.3 for each year of expirience

    # do it for 30 days, avarage month, later i can possibly create a function that will use specific numbers coresponding to the day in each specific month
    for i in range(30):
        results = simulate_single_day(staff_power, restaurant_reputation)
        gained_money += results[0]
        restaurant_reputation += results[1]

    return gained_money


def simulate_single_day(staff_power, restaurant_reputation):
    results = [0,0] # money and reputation 

    # get a chance for how many clients might show-up
    max_clients = restaurant_reputation // 50
    min_clients = restaurant_reputation // 100

    if min_clients < 1:
        min_clients = random.randint(0,1) # there is still a small chance that someone hungry will show-up
    
    if max_clients < 1:
        max_clients = 1

    clients = random.randint(min_clients, max_clients)
    customer_traffic = 0

    for i in range(clients):
        dish_worth = random.randint(5,100)
        customer_traffic += 1

        if customer_traffic > staff_power:
            results[1] = unhappy_client(results[1])
        else:
            results[1] = happy_client(results[1])
            results[0] += dish_worth

    return results


def happy_client(reputation):
    return reputation + 1 # happy restaurant review

def unhappy_client(reputation):
    return reputation - 1 # unhappy restaurant review

def chance_for_new_candidate(salary):

    # create random indywiduals
    people = []

    max_of_people = (salary - 3000) // 500
    number_of_people = random.randint(0,max_of_people)

    for i in range(number_of_people):
        expected_salary = random.randint(3000, 8000) # 3000 minimum, then increase to 3500 for that 500 window

        # only if salary is met, then add them to candidate list and give them names
        if salary >= expected_salary - 1000:

            genders = ["male", "female"]
            gender = random.choice(genders)
            name = "Scooby-Dooby Doo"
            if gender == "male":
                name = random.choice(male_names)
            elif gender == "female":
                name = random.choice(female_names)

            family_name = random.choice(family_names)
            age = random.randint(18,60)
            expirience = random.randint(0, 20)

            if age - expirience < 18:
                expirience = 0 # intern

            person = [name, family_name, age, expected_salary, expirience]
            people.append(person)
    
    return people # return all candidates