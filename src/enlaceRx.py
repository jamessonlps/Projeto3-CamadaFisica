from config.config import FAILURE_COMMUNICATION, SUCCESS_COMMUNICATION

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        return(len(self.buffer))

    def getAllBuffer(self, len):
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        # Ao começar a pegar o tempo, começa a cronometrar o tempo
        t0 = time.time()
        while(self.getBufferLen() < size):
            time.sleep(0.05)
            now = time.time()
            # Se o tempo estourar, retorna mensagem de falha na comunicação
            if now - t0 > 5 and self.getBufferLen() < size:
                return FAILURE_COMMUNICATION
        return(self.getBuffer(size))


    def clearBuffer(self):
        self.buffer = b""


