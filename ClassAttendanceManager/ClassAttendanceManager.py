import json
import time


class AttendanceList(object):
    def __init__(self):
        self.total_weeks = 16
        self.data = {}

        self.load_list()

    # Load students list
    def load_list(self):
        with open('list.json') as outfile:     
            data = json.load(outfile)
            
        self.data = data

    # Change total number of weeks shown in the list
    # Decreasing the list won't cause any data to be removed
    def change_total_weeks(self):
        valid = False
        new_total_weeks = ""
        while not valid:
            new_total_weeks = input("How many weeks?\n")

            try:
                new_total_weeks = int(new_total_weeks)
                valid = True
            except:
                print("Please enter a number!") 
        self.total_weeks = new_total_weeks

        print(f'Total weeks changed to {new_total_weeks}')

    @staticmethod
    def print_menu_options():
        print("""
                help    - Show help menu
                start   - Start attendance procedure
                list    - Show students list
                add     - Add a student
                del     - Delete a student
                search  - Search for students
                weeks   - Increase or Decrease total weeks (Default is 16)
                exit    - Exit the program
                reset   - Reset all data
            """)

    # Get the table header depending on total weeks
    def get_attendance_string(self):
        string = ""
        space_len = 4

        for i in range(self.total_weeks):
            string += "Week " + str(i + 1) + " " * (space_len - len(str(i+1)))
        return string

    # Clears the list.json file + some fun stuff :D
    def reset(self):
        print("Warning: This action is not recoverable!")
        confirm = input("Please send CONFIRM to reset everything!\n")
        if confirm == "CONFIRM":

            # Just to look cooler :D
            print("Reseting ...")
            for i in range(21):
                p = "=" * i
                s = " " * (20 - i)
                l = round((100 / 21) * (i + 1))
                print(f'[{p}{s}] - {l}%', end="\r")
                time.sleep(0.3)

            self.data = {}
            self.save_changes()
            print("\nCompleted!")

    # First part of table header
    def get_list_string(self):
        return "ID Name                      "

    # Save all the changes to list.json file
    def save_changes(self):
        with open('list.json', 'w') as json_file:  
            json.dump(self.data, json_file)

    def add_student(self):
        student_name = input("Please enter a name:\n")
        valid_id = False
        student_number = ""
        while not valid_id:
            student_number = input("Please enter student number (Example: 930234875):\n")
            if len(student_number) == 9:
                try:
                    int(student_number)
                    valid_id = True
                except:
                    pass
            if not valid_id:
                print("Student number should be a number with a length equal to 9")
        student_id = str(len(self.data.keys()) + 1)
        self.data[student_id] = {
            "ID": student_number,
            "Name": student_name,
            "attendances": []
        }

        self.save_changes()
        print("Student added :)")
    
    def delete_student(self):
        student_id = input("Enter student ID from list (Not student number!):\n")
        try:
            del self.data[student_id]
            self.save_changes()
            print("Student deleted :)")
        except:
            print("No such student!")
            
    def add_attendance(self, student_id, status, week):
        if len(self.data[student_id]["attendances"]) < week:
            for i in range(week - len(self.data[student_id]["attendances"])):
                self.data[student_id]["attendances"].append("-")

        self.data[student_id]["attendances"][week - 1] = status

    @staticmethod
    def get_attendance_status():
        valid_status = False
        status = ""
        while not valid_status:
            status = input("(A) absent or (P) present:\n")
            if status.lower() in ["a", "p"]:
                status = status.upper()
                valid_status = True
            else:
                print("Enter A for absent or B for present!")
        return status

    def do_attendance(self):
        valid_week = False
        week_number = 1
        while not valid_week:
            week_number = input("Week number:\n")
            try:
                week_number = int(week_number)
                if 0 < week_number <= self.total_weeks:
                    valid_week = True
                else:
                    print(f'Week number should be between 0 and {self.total_weeks + 1}')
            except:
                print("Week NUMBER!")
        mode = input("Enter 0 to loop over all students or enter student ID from list:\n")
        if mode == "0":
            for student in self.data:
                print(self.data[student]["Name"])
                status = self.get_attendance_status()
                self.add_attendance(student, status, week_number)
            print("All Done :)")
        else:
            if mode not in self.data.keys():
                print("No student found with that ID!")
            else:
                status = self.get_attendance_status()
                self.add_attendance(mode, status, week_number)
                print("Done :)")
        self.save_changes()

    def printstudents_list(self, students_list):
        id_len = 3
        name_len = 24
        string = ""
        for student in students_list:
            string += student + str(" " * (id_len - len(student)))
            string += students_list[student]["Name"] + " " * (name_len - len(students_list[student]["Name"]))
            for i in range(self.total_weeks):
                try:
                    string += " " * 4 + students_list[student]["attendances"][i] + " " * 4
                except:
                    string += " " * 4 + "-" + " " * 4
            string += '\n'
        print(string)

    def search(self):
        name = input("Please enter a name:\n")
        search_result = {}
        counter = 1

        for student_id in self.data:
            student = self.data[student_id]
            if student["Name"].lower() == name.lower() or name.lower() in student["Name"].lower():
                search_result[str(student_id)] = student
                counter += 1
        
        if len(search_result.keys()) > 0:
            print(self.get_list_string() + self.get_attendance_string())
            print(self.printstudents_list(search_result))

    def start(self):
        running = True
        self.print_menu_options()

        while running:
            command = input("Enter your command (help for menu):\n\n")

            if command.lower() == "help":
                self.print_menu_options()
            elif command.lower() == "start":
                self.do_attendance()
            elif command.lower() == "search":
                self.search()
            elif command.lower() == "list":
                print(self.get_list_string() + self.get_attendance_string())
                print(self.printstudents_list(self.data))
            elif command.lower() == "add":
                self.add_student()
            elif command.lower() == "del":
                self.delete_student()
            elif command.lower() == "exit":
                print("Bye Bye :)")
                running = False
            elif command.lower() == "weeks":
                self.change_total_weeks()
            elif command.lower() == "reset":
                self.reset()
                

def main():
    attendance_obj = AttendanceList()
    attendance_obj.start()


if __name__ == "__main__":
    main()
