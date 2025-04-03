from django.db import models

# Create your models here.

class Voter(models.Model):
    ''' Represents a registered voter  '''
    lastName = models.TextField()           # *    Last Name 
    firstName = models.TextField()          # *    First Name
    streetNumber = models.IntegerField()    # *    Residential Address - Street Number
    streetName = models.TextField()         # *    Residential Address - Street Name
    aptNumber = models.IntegerField()       # *    Residential Address - Apartment Number
    zipCode = models.IntegerField()         # *    Residential Address - Zip Code
    dob = models.CharField(max_length=10)   # *    Date of Birth
    dor = models.CharField(max_length=10)   # *    Date of Registration
    affiliation = models.CharField(max_length=2) # Party Affiliation (**note, this is a 2-character wide field**)
    precinctNumber = models.IntegerField()  # *    Precinct Number
    v20 = models.BooleanField()             # *    v20state
    v21s = models.BooleanField()            # *    v21town
    v21p = models.BooleanField()            # *    v21primary
    v22 = models.BooleanField()             # *    v22general
    v23 = models.BooleanField()             # *    v23town
    voterScore = models.IntegerField()      # *    Voter Score

    def __str__(self):
        ''' Returns a spring representation of a voter '''
        return f'{self.firstName} {self.lastName}, DOB: {self.dob}, Party: {self.affiliation}, Zipcode: {self.zipCode}'
    
    # begin load_data() function to process .csv file
    def load_data():
        '''Function to load data records from CSV file into Django model instances.'''

        filename = 'voter_analytics/data/newton_voters.csv'
        f = open(filename)
        f.readline() # discard headers

        for row in range(5):
            line = f.readline().strip()
            fields = line.split(',')
            # create a new instance of Voter object with this record from CSV
            voter = Voter(
                        lastName=fields[1],
                        firstName=fields[2],
                        streetNumber= fields[3],
                        streetName = fields[4],
                        aptNumber = fields[5],
                        zipCode = fields[6],
                        dob = fields[7],
                        dor = fields[8],
                        affiliation = fields[9],
                        precinctNumber = fields[10],
                        v20 = fields[11],
                        v21s = fields[12],
                        v21p = fields[13],
                        v22 = fields[14],
                        v23 = fields[15],
                        voterScore = fields[16]
                        )
            print(f'Created result: {voter}')
        
    