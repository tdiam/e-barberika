
## Έναρξη του HTTPS server

```
$ python manage.py runhttps 8443
```

H εφαρμογή (frontend και backend) είναι διαθέσιμη στο  `https://asoures.gr:8443/`.


## Έναρξη των development server

To frontend της εφαρμογής χρησιμοποιεί ReactJS, ενώ το backend είναι υλοποιημένο σε Django. Κάθε ένα από αυτά έχει τον δικό του development server. Αυτοί τρέχουν εντελώς εντελώς ανεξάρτητα σε ξεχωριστές πόρτες. Το μόνο που χρειάζεται είναι το frontend να γνωρίζει την διεύθυνση στην οποία είναι διαθέσιμο το backend API. Συνεπώς, για την εκκίνηση των development servers:

```
$ python manage.py runserver 8000           # Django ακούει στο http://localhost:8000

$ export REACT_APP_API_URL=http://localhost:8000/observatory/api/
$ cd project/client && npm run start        # ReactJS ακούει στο http://localhost:3000 
```

Ο Django server έχει επίσης ρυθμιστεί να σερβίρει και το frontend, εφόσον αυτό χτιστεί με `npm run build`. Για διευκόλυνση της διαδικασίας, υπάρχει η custom εντολή:

```
$ python manage.py runhttp 8000
```

O server ακούει στη διεύθυνση `http://localhost:8000/`
