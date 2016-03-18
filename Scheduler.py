#  File: Scheduler.py
#  Description: Organize processes to be executed
#  Student's Name: Minh-Tri Ho
#  Student's UT EID: mh47723
#  Course Name: CS 313E
#  Unique Number: 50940
#
#  Date Created: 03/11/16
#  Date Last Modified: 03/11/16

class Scheduler(object):
    def __init__(self):
        self.scheduling = []
        self.top = Queue("Top Level", 10)
        self.mid = Queue("Mid Level", 100)
        self.bot = Queue("Bot Level", 1000)

    def add(self, process):
        self.top.add(process)
        print("Add:", process)

    def run(self):
        print("___________ Processes Start Running ___________")

        while(not(self.top.isEmpty() and self.mid.isEmpty() and self.bot.isEmpty())):
            #Show which process will be analyzed and the current status of the queue
            self.showQueue()

            #Starting with the Top level, if not empty
            if(not(self.top.isEmpty())):
                self.proc(1)

            #If Top level is empty, then go to Mid Level
            elif(not(self.mid.isEmpty())):
                self.proc(2)

            #If Mid level is empty, go to Bottom level
            elif(not(self.bot.isEmpty())):
                self.proc(3)

        #Display the historical scheduling from the first one to the last one
        print(self.scheduling)

    def proc(self, id):
        #Top level
        if(id == 1):
            proc_curr = self.top.pop()
            level = self.top.level
        #Mid level
        elif(id == 2):
            proc_curr = self.mid.pop()
            level = self.mid.level
        #Bottom level
        elif(id == 3):
            proc_curr = self.bot.pop()
            level = self.bot.level

        time_left = proc_curr.pop()
        #Time requested goes over time alloted, has to decrease its level for the remaining time
        if(time_left > level):
            #Actualize the remaining time
            time_left -= level

            #Document the historical scheduling
            self.scheduling.append(str(proc_curr) +"(" +str(level) +")")

            #Adds back the remaining time to the process
            proc_curr.add(time_left)

            #Assign the process to the next level
            if(id == 1):
                self.mid.add(proc_curr)
            else:
                self.bot.add(proc_curr)
            print(str(proc_curr) +"blocked for I/O")
        else:
            self.scheduling.append(str(proc_curr) +"(" +str(time_left) +")")
            if(not(proc_curr.isEmpty())):
                if(id == 1):
                    self.top.add(proc_curr)
                elif(id == 2):
                    self.mid.add(proc_curr)
                elif(id == 3):
                    self.bot.add(proc_curr)
                print(str(proc_curr) +"is pre-empted")

    def peek(self):
        if(not(self.top.isEmpty())):
            return self.top.peek()
        elif(not(self.mid.isEmpty())):
            return self.mid.peek()
        elif(not(self.bot.isEmpty())):
            return self.bot.peek()
        return ""

    def showQueue(self):
        print("\nRunning", self.peek())
        print(self.top)
        print(self.mid)
        print(self.bot)

class Node(object):
    def __init__(self, list):
        self.list = str(list).strip().lstrip("[").rstrip("]").split(",")
        if(self.list == ['']):
            self.list = ['0']

    def add(self, time):
        self.list.insert(0, time)

    def peek(self):
        print(self.list)
        return((int)(self.list[0]))

    def set(self, time):
        self.list[0] = time

    def pop(self):
        return((int)(self.list.pop(0)))

    def isEmpty(self):
        return self.list == []

class Queue(object):
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.queue = []

    def isEmpty(self):
        return(self.queue == [])

    def add(self, obj):
        self.queue.append(obj)

    def peek(self):
        return(self.queue[0])

    def pop(self):
        return(self.queue.pop(0))

    def __str__(self):
        res = self.name + ": "
        if self.queue == []:
            res += "[]"
        else:
            for proc in self.queue:
                res += "[" +str(proc) +"]"
        return(res)

class Process(object):
    def __init__(self, id, duration, io_time_stamp):
        self.id = id
        self.duration = duration
        self.io_time_stamp = Node(io_time_stamp)
        if(self.io_time_stamp.peek() == 0):
            self.io_time_stamp.set(self.duration)


    def __str__(self):
        return("P" +str(self.id))

    def add(self, time):
        self.io_time_stamp.add(time)

    def pop(self):
        return(self.io_time_stamp.pop())

    def isEmpty(self):
        return self.io_time_stamp.isEmpty()

def main():
  src = open(".\Processes.txt", "r")
  sc = Scheduler()

  for line in src:
    data = line.strip().split(";")
    sc.add(Process(int(data[0]), int(data[1]), eval(data[2])))

  sc.run()

main()
