import icat, time, stomp, json, sys, re

class Client(object):
    def __init__(self, brokers, user, password, topics=None, consumer_name='QueueProcessor'):
        self._brokers = brokers
        self._user = user
        self._password = password
        self._connection = None
        self._topics = topics
        self._consumer_name = consumer_name
        self._listener = None

    def get_connection(self):
        connection = stomp.Connection(host_and_ports=self._brokers, use_ssl=True, ssl_version=3)
        connection.start()
        connection.connect(self._user, self._password, wait=False)

        time.sleep(0.5)
        return connection

    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            self._disconnect()
            self._connection = self.get_connection()

    def _disconnect(self):
        if self._connection is not None and self._connection.is_connected():
            self._connection.disconnect()
        self._connection = None

    def stop(self):
        self._disconnect()
        if self._connection is not None:
            self._connection.stop()
        self._connection = None

    def send(self, destination, message, persistent='true'):
        if self._connection is None or not self._connection.is_connected():
            self._disconnect()
            self._connection = self.get_connection()
        self._connection.send(destination, message, persistent=persistent)
        
        
activemq_client = Client([("autoreduce.isis.cclrc.ac.uk", 61613)], 'autoreduce', '1^G8r2b$(6', 'RUN_BACKLOG')
activemq_client.connect()

if len(sys.argv) < 4:
  min_run = int(raw_input('Start run number: '))
  max_run = int(raw_input('End run number: '))
  rename = raw_input('Use .nxs file? [Y/N]: ')
  rbnum = int(raw_input('RB Number: '))
  cycle = raw_input('Enter cycle number in format [14_3]: ')
else:
  min_run = int(sys.argv[1])
  max_run = int(sys.argv[2])
  rename = 'n' #change to use nxs file
  rbnum = int(sys.argv[3]) #test RB
  cycle = str(sys.argv[4])


instrument = 'WISH'
start = time.clock()
print "Start: %0.3f" % start

for x in range (min_run, max_run+1):
  location = str("\\isis\NDXWISH\Instrument\data\cycle_"+str(cycle)+"\WISH000"+str(x)+".raw")
  if rename.lower() == 'y':
    location = location.replace('.raw','.nxs')
  pattern = re.compile('(?P<before>cycle_\d\d_\d)\$', re.IGNORECASE)
  location = pattern.sub('\g<before>', location)
  data_dict = {
    "rb_number": str(rbnum),
    "instrument": instrument,
    "data": location,
    "run_number": str(int(x)),
    "facility": "ISIS"
    }
  activemq_client.send('/queue/DataReady', json.dumps(data_dict))
  print data_dict
  time.sleep(2)
