# Βοηθητικές συναρτήσεις για το API

Για την ανάπτυξη του API χρειάζονται κάποιες λειτουργίες που είναι κοινές για κάθε κομμάτι και ορίζονται στο `project/api/helpers.py`. Ακολουθεί το documentation τους:

* [`ApiMessage`](#apimessage)
* [`ApiResponse`](#apiresponse)


## ApiMessage

Για εύκολη επιστροφή JSON responses του στυλ `{"message": ...}`.

Το πρώτο όρισμα είναι το μήνυμα, ενώ τα υπόλοιπα είναι τα ίδια ορίσματα που δέχεται και το [`JsonResponse`](https://docs.djangoproject.com/en/2.1/ref/request-response/#jsonresponse-objects) του Django (πχ. `status`).

Οι χαρακτήρες UTF-8 δεν κωδικοποιούνται σε ASCII, αλλά εμφανίζονται όπως είναι.

### Παράδειγμα: Μήνυμα με error 400

Κώδικας:
```python
class MyView(View):
    def post(self, request):
        ...
        return ApiMessage('Το πεδίο "title" είναι υποχρεωτικό.', status=400)
```

Επιστρέφει:
```json
{
    "message": "Το πεδίο \"title\" είναι υποχρεωτικό."
}
```


## ApiResponse

Επιστρέφει JSON responses, επιτρέποντας το πέρασμα Django models ως δεδομένα.

Για να γίνει αυτό, πρέπει να ορίσετε στα models τη συνάρτηση `__serialize__`. Ο ρόλος της `__serialize__` είναι να επιστρέψει τις πληροφορίες του model σε μορφή αντικειμένων που ο JSON encoder ξέρει πώς να μετατρέψει σε JSON (dict, list, tuple, str, int, float, boolean).

Εφόσον τα models σας έχουν υλοποιήσει την `__serialize__`, τότε μπορείτε να χρησιμοποιήσετε την `ApiResponse` για να επιστρέψετε model instances, λίστες από instances ή querysets σε μορφή JSON.

Όπως και προηγουμένως, η `ApiResponse` μπορεί να δεχθεί τα ίδια ορίσματα με αυτά της `JsonResponse` και οι χαρακτήρες UTF-8 δεν μετατρέπονται σε ASCII.

### Παράδειγμα

Κώδικας:
```python
class Article(models.Model):
    ...
    def __serialize__(self):
        return OrderedDict(
            title=self.title,
            content=self.content
        )

class MyView(View):
    def get(self, request):
        data = {
            "start": 0,
            "count": 20,
            "articles": Article.objects.all()[:20]
        }
        return ApiResponse(data)
```

Επιστρέφει:
```json
{
    "start": 0,
    "count": 20,
    "articles": [
        {
            "title": "First article",
            "content": "Lorem ipsum dolor sit amet"
        },
        {
            ...
        },
        ...
    ]
}
```

### Προσαρμογή της `__serialize__`

Η `__serialize__` μπορεί να δεχθεί και ειδικά arguments ώστε να αλλάζει η λειτουργικότητά της ανάλογα με αυτά.

Για να της περάσετε arguments, χρησιμοποιήστε το όρισμα `serialize_args` στην `ApiResponse`.

#### Παράδειγμα

```python
class Article(models.Model):
    ...
    def __serialize__(self, capitalize=False):
        title = self.title
        if capitalize:
            title = title.capitalize()

        return OrderedDict(
            title=title,
            content=self.content
        )

class MyView(View):
    def get(self, request):
        ...
        return ApiResponse(article, serialize_args={'capitalize': True})
```