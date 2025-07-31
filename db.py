import psycopg2


def connect():
    dsn = "postgresql://postgres:ZZWLoynvISALiFtDYbfHiOEEwOlkMkyx@mainline.proxy.rlwy.net:43779/railway"
    return psycopg2.connect(dsn)
