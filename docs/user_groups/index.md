# Ομάδες χρηστών

Στο παρατηρητήριο υπάρχουν 3 ομάδες χρηστών:

* **Ανώνυμοι:**  
  Έχουν πρόσβαση μόνο στα endpoints ανάκτησης και αναζήτησης πληροφοριών. Στο Django αναπαρίστανται ως χρήστες που δεν έχουν λογαριασμό (anonymous user).
* **Εθελοντές:**  
  Έχουν πρόσβαση σε όσα έχουν και οι Ανώνυμοι, καθώς και στα endpoints δημιουργίας, ενημέρωσης και απόσυρσης (`withdrawn=True`) καταχωρήσεων. Στο Django αναπαρίστανται ως χρήστες που ανήκουν στο ορισμένο από εμάς group `Volunteer`.
* **Διαχειριστές:**  
  Έχουν πρόσβαση σε όσα έχουν και οι Εθελοντές, καθώς και στα endpoints οριστικής διαγραφής καταχωρήσεων. Στο Django αναπαρίστανται ως χρήστες που έχουν `is_staff=True`, δηλαδή μπορούν να συνδεθούν στη διαχειριστική πλατφόρμα.

## Βοηθητικές συναρτήσεις για views

Στο `project/api/helpers.py` ορίζουμε τις εξής βοηθητικές συναρτήσεις:

* `is_volunteer(request)`:  
  Επιστρέφει μία boolean τιμή που δείχνει αν ο χρήστης του request είναι Εθελοντής ή Διαχειριστής.
* `is_admin(request)`:  
  Επιστρέφει μία boolean τιμή που δείχνει αν ο χρήστης του request είναι Διαχειριστής.
* `@volunteer_required`:  
  Decorator που περιορίζει την πρόσβαση σε ένα view function μόνο σε χρήστες με δικαιώματα Εθελοντή. Αν ο χρήστης δεν έχει τέτοια δικαιώματα, τότε επιστρέφεται αυτόματα HTTP response με κωδικό 401 (Unauthorized).
* `@admin_required`:  
  Παρόμοιος decorator με τον παραπάνω που περιορίζει την πρόσβαση σε χρήστες με δικαιώματα Διαχειριστή.

### Παραδείγματα χρήσης

#### Για view functions
```python
@volunteer_required
def simple_view(request):
    return HttpResponse('Αυτό το βλέπουν μόνο εθελοντές')
```

#### Για class-based views
```python
from django.utils.decorators import method_decorator

class MyView(View):
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return HttpResponse('Αυτό το βλέπουν μόνο διαχειριστές')
```