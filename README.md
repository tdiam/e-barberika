# Asoures

Project σε Django για το μάθημα της [Τεχνολογίας Λογισμικού](https://courses.softlab.ntua.gr/softeng/2018b/) της Σχολής ΗΜΜΥ ΕΜΠ.

## Ομάδα

Η ομάδα Asoures σε αλφαβητική σειρά:

1. Θοδωρής Διαμαντίδης - 03115007
1. Άγγελος Κολαΐτης - 03115029
1. Νίκος Λούκας - 03115188
1. Βασίλης Ξανθόπουλος - 03115186
1. Γιώργος Χοχλάκης - 03115133

## Deployment

Για deploy της εφαρμογης:

```
# σεταρισμα του περιβαλλοντος, εγκατασταση πακετων, βασης, κλπ
$ export DEBUG=no
$ ./deploy.sh

# εναρξη του server
$ venv/bin/python manage.py runhttps 8443
```

## Documentation

* [Κανόνες συνεισφοράς](docs/contributing.md)
* [Εγκατάσταση](docs/installation.md)
* [Δομή project](docs/structure.md)
* [Χρήση](docs/usage.md)
* Υποσυστήματα:
  * [Tests](docs/tests.md)
  * [Client](docs/client/index.md)
  * [Token Auth](docs/token_auth/index.md)
  * [API helpers](docs/api_helpers/index.md)
  * [Ομάδες χρηστών](docs/user_groups/index.md)
  * [SSL](docs/ssl.md)
* [1ο Παραδοτέο](docs/deliverable1.md)
* [2ο Παραδοτέο](docs/deliverable2.md)
