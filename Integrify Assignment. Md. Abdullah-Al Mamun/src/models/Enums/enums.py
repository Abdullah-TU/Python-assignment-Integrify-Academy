from enum import Enum
# todo list statuses enum values
class status(str,Enum):
   NotStarted = 'NotStarted'
   OnGoing = 'OnGoing'
   Completed = 'Completed'
