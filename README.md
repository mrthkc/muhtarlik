# Mahallenin Muhtarları, Çiçek Taksi, Kaygısızlar #

## Environment ##
Check parameters and make necessary changes.

```cp environment.sample .env```

## Install ##
Install python 3.8.10

* ```python3.8 -m venv venv```

* ```./venv/bin/python3.8 -m pip install -r requirements.txt```

## Run Service ##

* ```./venv/bin/uvicorn main:app --reload```

Please navigate to **<http:localhost:8000/docs>**