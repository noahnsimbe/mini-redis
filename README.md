# Mini Redis

This is a simplified version of Redis implemented using Flask.

## Main Features
- Data Storage: An in-memory storage for key-value pairs.
- Supported Commands:
  - SET key value: Stores the key-value pair in the database.
  - GET key: Retrieves the value associated with the key.
  - DEL key: Deletes the key-value pair from the database.
  - EXPIRE key seconds: Sets a timeout on the specified key. After the timeout has expired, the key should be deleted.
  - TTL key: Returns the remaining time to live of a key that has an expiration set, in seconds.
- Persistence:
  - A simple mechanism to persist the data to a json file
  - Data reloads on server start.
- Networking: A simple TCP server that handles incoming requests and send responses.
- Concurrency: Multiple clients can connection simultaneously.

## Running without a script
### Setup

1. Clone the repository:
```bash
git clone https://github.com/noahnsimbe/mini-redis.git
cd mini-redis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create a `.env` file using contents of the env.example:
```bash
cp env.example .env
```

### Start the server:
```bash
python app.py
```

<span style="color:red">**The server will be accessible at [`http://localhost:5000`](http://localhost:5000)**</span>

## Running using a script

###  Make the `run.sh` script executable:
```bash
chmod +x run.sh
```

### Start the server:
```bash
./run.sh
```

<span style="color:red">**The server will be accessible at [`http://localhost:5000`](http://localhost:5000)**</span>

## API Documentation

API documentation is available at [`http://localhost:5000/apidocs`](http://localhost:5000/apidocs).
