import csv

leave = False

while not leave:
# Make a list of all exports and imports
    data = []
    with open('synergy_logistics_database.csv', 'r') as table:
        reader = csv.reader(table)

        for row in reader:
            data.append(row)
        
    def routes(direction):
        counter = 0
        counted_routes = []
        routes = []
        sum_value = 0
        average_value = 0
        top10_routes = []

        # Create a list of routes ['origin', 'destination', times_repited, total_value, average_value_per_route]
        for route in data:
            if route[1] == direction:
                current_route = [route[2], route[3]]
                if current_route not in counted_routes:
                    for movement in data:
                        if current_route == [movement[2], movement[3]]:
                            counter += 1
                            sum_value += int(movement[9])
                    average_value = sum_value / counter

                    counted_routes.append(current_route)
                    routes.append([route[2], route[3], counter, sum_value, round(average_value, 2)])
                    counter = 0
                    sum_value = 0

        
        # Sort the list by the average value per route
        length = len(routes)
        for i in range(0, length): 
            for j in range(0, length-i-1): 
                if (routes[j][4] < routes[j + 1][4]): 
                    routes[j], routes[j + 1] = routes[j + 1], routes[j]
        
        # Create a list with only the first ten valueble routes
        for route in routes:
            if counter <= 9:
                top10_routes.append(route)
                counter += 1
        
        return top10_routes

    def transport(direction):
        counter = 0
        counted_transport = []
        transport_mode = []
        sum_value = 0
        average_value = 0

        # Create a list of transport mode
        for route in data:
            if route[1] == direction:
                current_trasport = route[7]
                if current_trasport not in counted_transport:
                    for movement in data:
                        if current_trasport == movement[7]:
                            counter += 1
                            sum_value += int(movement[9])
                    average_value = sum_value / counter

                    counted_transport.append(current_trasport)
                    transport_mode.append([route[7], counter, sum_value, round(average_value, 2), direction])
                    counter = 0
                    sum_value = 0
        # Sort the list from the most valueble transport mode to the less repited
        length = len(transport_mode)
        for i in range(0, length): 
            for j in range(0, length-i-1): 
                if (transport_mode[j][3] < transport_mode[j + 1][3]): 
                    transport_mode[j], transport_mode[j + 1] = transport_mode[j + 1], transport_mode[j]
        return transport_mode

    def value():
        data.pop(0)
        counter = 0
        counted_countries = []
        countries = []
        sum_value = 0
        average_value = 0
        directions = []
        no_repeting_directions = []
        exports_countries = []
        imports_countries = []
        total_value = 0
        stack = 0
        sorted_countries = []
        final_percent = 0

        # Create a list of directions with out repeting
        for direction in data:
            directions.append(direction[1])
            for direction in directions:
                if direction not in no_repeting_directions:
                    no_repeting_directions.append(direction)

        # Create a list of countries for each direction
        for direction in no_repeting_directions:
            for route in data:
                if direction == 'Exports':
                    current_country = route[2]
                    if current_country not in counted_countries:
                        for movement in data:
                            if current_country == movement[2]:
                                counter += 1
                                sum_value += int(movement[9])
                        average_value = sum_value / counter

                        counted_countries.append(current_country)
                        exports_countries.append([route[2], counter, sum_value, round(average_value, 2), direction])
                        counter = 0
                        sum_value = 0  
                elif direction == 'Imports':
                    current_country = route[3]
                    if current_country not in counted_countries:
                        for movement in data:
                            if current_country == movement[3]:
                                counter += 1
                                sum_value += int(movement[9])
                        average_value = sum_value / counter
                        counted_countries.append(current_country)
                        imports_countries.append([route[3], counter, sum_value, round(average_value, 2), direction])
                        counter = 0
                        sum_value = 0

        # Make a list of all the countries 
        countries = exports_countries + imports_countries                    
                    
        # Sort the list by the average value in each route
        length = len(countries)
        for i in range(0, length): 
            for j in range(0, length-i-1): 
                if (countries[j][3] < countries[j + 1][3]): 
                    countries[j], countries[j + 1] = countries[j + 1], countries[j]
        
        # Sum all the values, then find the 80% of it
        for country in countries:
            total_value += country[2]
        eighty_percent_value = total_value * .8

        # Create a list with only the countries that make around the 80% of revenue in the company
        for country in countries:
            if stack <= eighty_percent_value:
                stack += country[2]
                sorted_countries.append(country)

        # Find the exact percentage of the revenue of the countries list
        final_percent = round((stack * 100)/total_value, 2)
        print('\nThe exact porcentange is', final_percent, 'percent.')

        return sorted_countries

    # Show a menu to choose what the user wants to do
    options = input('\n1-Top 10 routes.\n2-Bests transport modes.\n3-Countries that generates the 80 percent of the revenue\n4-Leave\nPlease choose an option to show what you what to see: ')

    # Show the top 10 routes depending on the direction
    if options == '1':
        choice = input('1-Exportations\n2-Importations\nPlease select one direction: ')
        if choice == '1':
            data = routes('Exports')
            print('\n\nTop 10 routes are:\n')
            route_index = 1
            for i in range(len(data)):
                print(route_index, '-', data[i][0], '-', data[i][1], 'with an average revenue per travel of $', data[i][4], 'traveling' , data[i][2],'times, and with a total revenue of $', data[i][3])
                route_index += 1
        elif choice == '2':
            data = routes('Imports')
            print('\n\nTop 10 routes are:\n')
            route_index = 1
            for i in range(len(data)):
                print(route_index, '-', data[i][0], '-', data[i][1], 'with an average revenue per travel of $', data[i][4], 'traveling' , data[i][2],'times, and with a total revenue of $', data[i][3])
                route_index += 1
        else:
            print('You choose a wrong option\n')
    
    # Show the bests transport modes depending on the direction
    elif options == '2':
        choice = input('1-Exportations\n2-Importations\nPlease select one direction: ')
        if choice == '1':
            data = transport('Exports')
            print('\n\nBest transport modes:\n')
            route_index = 1
            for i in range(len(data)):
                print(route_index, '-', data[i][0], 'traveling', data[i][1], 'times, and with an average revenue per travel of $', data[i][3])
                route_index += 1
        elif choice == '2':
            data = transport('Imports')
            print('\n\nBest transport modes:\n')
            route_index = 1
            for i in range(len(data)):
                print(route_index, '-', data[i][0], 'traveling', data[i][1], 'times, and with an average revenue per travel of $', data[i][3])
                route_index += 1
        else:
            print('You choose a wrong option\n')

    # Show the countries that generates the 80 percent of the total revenue
    elif options == '3':
        data = value()
        print('Countries that generates the 80 percent of the revenue: \n')
        route_index = 1
        for i in data:
            print(route_index, '-', i[0], 'being an', i[4], 'country, with an average revenue per travel of $', i[3], 'traveling', i[1] , 'times and with a total revenue of $', i[2])
            route_index += 1

    # Change the flag 'leave' to true so, the while and the program finish
    elif options == '4':
        leave = True

    else:
        print('You choose a wrong option\n')