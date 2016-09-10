ta_data = [('Peter', 'USA', 'CS262'),
           ('Andy', 'USA', 'CS212'),
           ('Sarah', 'England', 'CS101'),
           ('Gundega', 'Lativa', 'CS373'),
           ('Job', 'USA', 'CS387'),
           ('Sean', 'USA', 'CS253')]

ta_countrys = [name + ' lives in ' + country for name, country, course in ta_data]

for row in ta_countrys:
    print row

