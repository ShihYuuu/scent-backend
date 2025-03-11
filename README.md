# Flask + MySQL

## Create Database
1. Download MySQL (MacOS)
```=bash
brew install mysql
```
2. Start the sql server in terminal
```=bash
brew services start mysql
```
3. Download DBeaver
```
brew install dbeaver
```
4. Create Database in DBeaver
```=sql
CREATE DATABASE scent;
USE scent;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255) NOT NULL
);
```

## Run the server
1. Install all requirements
```=bash
pip install -r requirements.txt
```

2. Run the program
```=bash
python app.py
```