from django.db import models

# Create your models here.

class Voter(models.Model):
    ''' Represents a registered voter  '''
    lastName = models.TextField()           # *    Last Name 
    firstName = models.TextField()          # *    First Name
    streetNumber = models.TextField()    # *    Residential Address - Street Number
    streetName = models.TextField()         # *    Residential Address - Street Name
    aptNumber = models.TextField()       # *    Residential Address - Apartment Number
    zipCode = models.TextField()         # *    Residential Address - Zip Code
    dob = models.CharField(max_length=10)   # *    Date of Birth
    dor = models.CharField(max_length=10)   # *    Date of Registration
    affiliation = models.CharField(max_length=2) # Party Affiliation (**note, this is a 2-character wide field**)
    precinctNumber = models.TextField()  # *    Precinct Number
    v20 = models.BooleanField()             # *    v20state
    v21s = models.BooleanField()            # *    v21town
    v21p = models.BooleanField()            # *    v21primary
    v22 = models.BooleanField()             # *    v22general
    v23 = models.BooleanField()             # *    v23town
    voterScore = models.TextField()      # *    Voter Score

    def __str__(self):
        ''' Returns a spring representation of a voter '''
        if len(self.affiliation) == 2 and self.affiliation[1] == ' ':
            party = self.affiliation[0]
        else:
            party = self.affiliation
        return f'{self.firstName} {self.lastName}| DOB: {self.dob}, Party: {party}, Zipcode: {self.zipCode}'
    
    # begin load_data() function to process .csv file
    def load_data():
        '''Function to load data records from CSV file into Django model instances.'''

        filename = 'voter_analytics/data/newton_voters.csv'
        f = open(filename)
        f.readline() # discard headers
        for line in f:
            fields = line.strip().split(',')
            # create a new instance of Voter object with this record from CSV
            try:
                voter = Voter(
                            lastName=fields[1],
                            firstName=fields[2],
                            streetNumber=fields[3] if fields[3] else "N/A",
                            streetName=fields[4],
                            aptNumber=fields[5] if fields[5] else "N/A",
                            zipCode=fields[6] if fields[6] else "N/A",
                            dob=fields[7],
                            dor=fields[8],
                            affiliation=fields[9].strip(),
                            precinctNumber=fields[10] if fields[10] else "N/A",
                            v20=fields[11].strip().upper() == "TRUE",
                            v21s=fields[12].strip().upper() == "TRUE",
                            v21p=fields[13].strip().upper() == "TRUE",
                            v22=fields[14].strip().upper() == "TRUE",
                            v23=fields[15].strip().upper() == "TRUE",
                            voterScore=fields[16] if fields[16] else "N/A"
                            )
                voter.save() # commit to database
                print(f'Created voter: {voter}')

            except Exception as e:
                print(f"Skipped: {fields} → {e}")
        print(f'Done. Created {len(Voter.objects.all())} voters.')
        f.close()

        
    