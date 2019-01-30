# Testing

Το API συνοδεύεται και από έναν αριθμό από tests που εξασφαλίζουν την ορθότητα της λειτουργίας του. Χωρίζονται σε δύο κατηγορίες:

* **Unit Tests**: Για κάθε στοιχείο του API υπάρχουν test που ελέγχουν την ορθότητά του ως κλειστό κουτί, ανεξάρτητα από το υπόλοιπο σύστημα.
* **Integration Tests**: Βασισμένο στον [test client](1), τρέχει ένα σενάριο διαδοχικών ενεργειών ενός χρήστη και ελέγχει ότι το σύστημα συμπεριφέρεται όπως πρέπει.

## Unit Tests

Για την εκτέλεση των unit tests:

```
python manage.py test
```

## Integration Tests

Για την εκτέλεση των integration tests:

```
python manage.py integration_test
```

Το οποίο είναι ισοδύναμο με το:

```
python manage.py test project.api.tests.integration.IntegrationTests.IntegrationTests
```

[1]: https://github.com/saikos/softeng18b-rest-api-client/tree/master/src/test/groovy/gr/ntua/ece/softeng18b/client