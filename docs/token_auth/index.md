# Token Auth

Το Token Auth μας επιτρέπει να δίνουμε στους χρήστες του API ένα αναγνωριστικό (token) κατά την πρώτη τους σύνδεση, ώστε να το χρησιμοποιούν σε όλες τις επόμενες κλήσεις τους προς το API, χωρίς να χρειάζεται να ξανασυνδεθούν.

## Πώς λειτουργεί;

* Ο χρήστης συνδέεται αρχικά μέσω ενός endpoint που ορίζει η εφαρμογή με username, password. Η πιστοποίηση γίνεται με το προεπιλεγμένο σύστημα του Django για τους χρήστες [[1]](https://docs.djangoproject.com/en/2.1/topics/auth/default/). Ο server απαντάει με το [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) token σε μορφή JSON:
   ```json
   {
       "token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   }
   ```
* Ο χρήστης αποθηκεύει το token και το χρησιμοποιεί στις κλήσεις του API, ορίζοντάς το στο HTTP Header `X-TOKEN-AUTH`:
   ```
   POST / HTTP/1.1
   Host: localhost
   ...
   X-TOKEN-AUTH: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ...
   ```
* Το Token Auth έχει ορίσει ένα [middleware](https://docs.djangoproject.com/en/2.1/topics/http/middleware/) που όταν εντοπίζει το header `X-TOKEN-AUTH`, προσπαθεί να κάνει πιστοποίηση μέσω του token. Αυτή η πιστοποίηση έχει υλοποιηθεί από το Token Auth ως [custom backend](https://docs.djangoproject.com/en/2.1/topics/auth/customizing/).

## Χρήση

### Για περιορισμό πρόσβασης σε views
Όλοι οι [τρόποι περιορισμού πρόσβασης](https://docs.djangoproject.com/en/2.1/topics/auth/default/#limiting-access-to-logged-in-users) που προσφέρει από προεπιλογή το Django εξακολουθούν να ισχύουν.

Παράδειγμα:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Todo

class AddTodo(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get('name')
        t = Todo(name=name)
        t.save()
```

### Για τους χρήστες του API
Το μόνο που χρειάζεται είναι να ληφθεί το token και μετά να χρησιμοποιηθεί σε επόμενα αιτήματα μέσω του header `X-TOKEN-AUTH`.

Παράδειγμα:
```python
import requests

# Get token
r = requests.post('http://localhost:8000/api/login/', data={
    'username': 'johndoe',
    'password': 'johndoe'
})
token = r.json()['token']

# Use token for a random request
payload = {'name': 'Walk the dog'}
headers = {
    'X-TOKEN-AUTH': token
}

# Add a todo item
r = requests.post('/api/todo', data=payload, headers=headers)
```

## Ρυθμίσεις

Οι ρυθμίσεις του Token Auth ορίζονται στο settings file του Django project και είναι οι εξής:

* `TOKEN_AUTH_URL_PREFIX`  
  Η επαλήθευση μέσω token θα ισχύει μόνο για URLs που ξεκινούν με το δηλωμένο prefix.

  Παράδειγμα:
   ```python
   TOKEN_AUTH_URL_PREFIX = '/api/'
   ```

  Αν δεν οριστεί, τότε θα πάρει την τιμή του `API_ROOT`. Αν ούτε αυτό οριστεί θα είναι `/`, δηλαδή η επαλήθευση θα ισχύει για όλες τις διευθύνσεις.

* `TOKEN_AUTH_HEADER`  
  Ο header στον οποίο ο χρήστης θα δίνει το token του.
  
  Αν ο header είναι ο `X-ABC-DEF`, η τιμή της ρύθμισης θα πρέπει να είναι `HTTP_X_ABC_DEF`, δηλαδή να ξεκινάει με `HTTP` και οι παύλες να αντικατασταθούν από underscores.

  Παράδειγμα:
   ```python
   TOKEN_AUTH_HEADER = 'HTTP_X_ABC_DEF'
   ```

  Default τιμή: `HTTP_X_TOKEN_AUTH`.

* `TOKEN_EXPIRATION`  
  Ένα dictionary που αναπαριστά τη διάρκεια χρόνου για την οποία τα tokens είναι έγκυρα. Οι τιμές των κλειδιών είναι οι ίδιες με τα ορίσματα των [timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) στην Python.

  Τα tokens που έχουν ξεπεράσει τη διάρκεια, ακυρώνονται και διαγράφονται αυτόματα.

  Παράδειγμα:
   ```python
   TOKEN_EXPIRATION = {
       'hours': 2,
       'minutes': 30
   }
   ```

  Default τιμή: `{'hours': 1}`.
