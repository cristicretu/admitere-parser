import os
import sys

from pypdf import PdfReader

data_array = []

def isLetter(c):
  return c.islower() or c.isupper()

class DataObject:
    def __init__(self, ID, Discipline, Grade):
        self.ID = ID
        self.Discipline = Discipline
        self.Grade = Grade

if __name__ == "__main__":
    res = sys.argv[1]
    if not os.path.exists(res):
        print ("File not found")
        sys.exit(1)

    pdf = PdfReader(res)
    counter = 0

    with open(res, 'rb') as file:
        reader = PdfReader(file)
        pages = len(reader.pages)

        for i in range(pages):
            page_text = reader.pages[i].extract_text()

            for line in page_text.split('\n'):
               line = line.strip()
               counter += 1

               # ignore the first 5 lines, they are not grades
               if counter < 6:
                   continue

               pos = max(line.find('I'), line.find('M'))
               id_pos = pos - 8
               id = line[id_pos:id_pos+8]
               id = id.replace(' ', '')

               if line.find('I') > -1:
                    discipline = 'Informatica'
               else:
                    discipline = 'Matematica'

               grade = ''
               grade = line[-10:]

               grade = grade.replace(' ', '')
               grade = ''.join([c for c in grade if c.isdigit() or c == '.'])

               if grade:
                  data_array.append(DataObject(id, discipline, float(grade)))

    # remove items with no grade
    data_array = [x for x in data_array if x.Grade != '']

    # sort by grade
    data_array.sort(key=lambda x: x.Grade, reverse=True)

    # is sys.argv[2] starts with I, then only show disciplines that start with I
    # if sys.argv[2].startswith('i') or sys.argv[2].startswith('I'):
    #     data_array = [x for x in data_array if x.Discipline.startswith('I')]
    # elif sys.argv[2].startswith('m') or sys.argv[2].startswith('M'):
    #     data_array = [x for x in data_array if x.Discipline.startswith('M')]
    # else:
    #     data_array = [x for x in data_array if x.Discipline.startswith(sys.argv[2])]

    if len(sys.argv) > 3:
        data_array = data_array[:int(sys.argv[3])]
    else:
        data_array = data_array

    # for data_obj in data_array:
    #   print(data_obj.ID, data_obj.Discipline, data_obj.Grade)    

    # create a new file with the results
    with open('results.txt', 'w') as file:
      for index, (data_obj) in enumerate(data_array):
         file.write(str(index) + ' ' + data_obj.ID + ' ' + data_obj.Discipline + ' ' + str(data_obj.Grade) + '\n')