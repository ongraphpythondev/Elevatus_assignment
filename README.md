# Elevatus 
In this project a user with authentication can perform a crud of candidates and download candidates in a csv file


### Clone project use follwing command
```
git clone https://github.com/ongraphpythondev/Elevatus.git
```

### Create a virtual enviorment and activate it
```
python -m venv venv
source venv/bin/activate
```

### To run this on localhost

# Install dependencies to run the project
```
pip install -r requirments.txt
```

# Run the project
```
uvicorn main:app --reload
```

### To run this on docker
You should have docker installed in your system
```
docker-compose build
docker-compose up -d
```