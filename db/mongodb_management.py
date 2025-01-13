import pymongo
from config import loader
# MongoDB connection parameters
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "myapp"
COLLECTION_NAME = "users"

myConf = loader.Configer()

class MongoDBConnection:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            host=myConf.get('mongodb','host'),
            port=int(myConf.get('mongodb', 'port')),
            username=myConf.get('mongodb','username'),
            password=myConf.get('mongodb','password')
        )
        self.db = self.client[str(myConf.get('mongodb','database'))]

    def close_connection(self):
        self.client.close()




class MongoDBManagement:
    def __init__(self) -> None:
        self.client = MongoClient(
            host=myConf.get('mongodb', 'host'),
            port=int(myConf.get('mongodb', 'port')),
            username=myConf.get('mongodb', 'username'),
            password=myConf.get('mongodb', 'password')
        )
        self.db = self.client[str(myConf.get('mongodb', 'database'))]

    def close_connection(self):
        self.client.close()

    def execute_aggregation_query(self, pipeline, collection_name="user"):
        result = self.db[collection_name].aggregate(pipeline=pipeline)
        return result

    def execute_count_document_query(self, condition, collection_name="user"):
        result = self.db[collection_name].count_documents(condition)
        return result

    def get_timespan(self, timespan_type: str = "period", period_type: str = "M",
                     period_value: int = 1, start_timestamp: Union[int, None] = None,
                     end_timestamp: Union[int, None] = None):
        if timespan_type == 'period':
            boundaries = self.get_timespan_by_period(period_type=period_type,
                                                     period_value=period_value)
        elif timespan_type == 'date':
            boundaries = self.get_timespan_by_date(start_timestamp=start_timestamp,
                                                   stop_timestamp=end_timestamp)
        else:
            return []
        return boundaries

    def get_timespan_by_period(self, period_type, period_value):
        now = datetime.now()
        stop = now
        start = now
        if period_type == 'w':
            start = now - timedelta(weeks=period_value)
        elif period_type == 'd':
            if period_value > 0:
                start = now - timedelta(days=period_value)
            else:
                total_min = datetime.now(timezone.utc).minute + datetime.now(timezone.utc).hour * 60
                total_second = total_min * 60
                if period_value == -1:
                    start = int(datetime.timestamp(
                        datetime.now())) - total_second
                    stop = start - (1 * 24 * 60 * 60)
                    every = abs(int((stop - start) / self.bar_count))
                    return self.generate_boundaries(start, stop, every)
        elif period_type == 'h':
            start = now - timedelta(hours=period_value)
        elif period_type == 'M':
            start = now - timedelta(days=(31 * period_value))
        elif period_type == 'm':
            start = now - timedelta(minutes=period_value)
        start = int(datetime.timestamp(start))
        stop = int(datetime.timestamp(stop))
        every = abs(int((stop - start) / self.bar_count))
        return self.generate_boundaries(start, stop, every)

    def get_timespan_by_date(self, start_timestamp, stop_timestamp):
        now = int(datetime.timestamp(datetime.now()))
        start = start_timestamp
        stop = stop_timestamp
        if stop > now:
            stop = now
        every = abs(int((stop - start) / self.bar_count))
        return self.generate_boundaries(start, stop, every)

    def set_bar_count(self, bar_count):
        self.bar_count = bar_count - 1

    def generate_boundaries(self, start, stop, every):
        boundaries = []
        for i in range(self.bar_count + 1):
            boundaries.append((start + (i * every)) * 1000)
        return boundaries
