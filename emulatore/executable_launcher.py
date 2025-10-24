import serial

ser = serial.Serial()
ser.baudate = 9600
ser.port = 'COM4'
ser.write_timeout = 1
ser.open()

fileInName = '../file/executable/emulator_executable.txt'
fileIn = open(fileInName,'r')

#while True:
    #ch=input()
    #ser.write(bytes(ch,'utf-8'))
    #receivedChar = ser.read().decode('utf-8')
    #print(receivedChar)

phase = 0
sinCosSent = 0
sinCosNumb=0
stateNumb = 0
riga = 0
for line in fileIn:
    print("Riga: " + format(riga) + "\n")
    riga+=1
    print(line)
    print(phase)
    if phase == 0:
        sinCosNumb = int(line)
        message = '?' + line[:-1] + '#'
        phase = 1

    elif phase == 1:

        stateNumb = 8
        message = '*' + line[:-1] + '#'
        if sinCosNumb == 0:
            phase = 3
        else:
            phase = 2

    elif phase == 2:
        message = '<' + line[:-1] + '#'
        sinCosSent += 1

        if sinCosSent==sinCosNumb:
            phase = 3
            print("I have to reach phase 3\n")

    elif phase == 3:

        message = '>' + line[:-1] + '#'

    try:
        for ch in message:
            ser.write(bytes(ch,'utf-8'))
    except serial.SerialTimeoutException:
        print("Write operation timed out!")
    print(ser.out_waiting)
    print(ser.in_waiting)
    if ser.in_waiting > 0:
        ser.reset_input_buffer()

ch = '!'
print(message)
ser.write(bytes(ch,'utf-8'))

print("Transmission Done")

fileIn.close()

fileOutName = '../file/executable/emulator_result.txt'
fileOut = open(fileOutName,'w')

lineCount = 0
newLine = False
while lineCount < stateNumb:

    receivedChar = ser.read().decode('utf-8')
    print("Received" + str(receivedChar))
     
    if receivedChar == '\n':
        if not(newLine):
            newLine=True
            receivedChar=' '
        else:
            newLine=False
            lineCount+=1
    
    fileOut.write(receivedChar)
   
    
    #line = ser.readline()
    #fileOut.write(str(line))
    #print(line)
    #line = ser.readline()
    #fileOut.write(str(line))
    #print(line)

fileOut.close()
ser.close()