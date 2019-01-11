# Χρηση SSL

Το HTTP δεν ειναι ασφαλες πρωτοκολλο, καθως τα δεδομενα που διακινουνται μεταξυ client και server φαινονται ως plain text σε ολη την διαδρομη αναμεσα τους (οποτε μπορει ο οποισδηποτε να διαβασει ευαισθητα δεδομενα, π.χ. κωδικους).

Για το λογο χρησιμοποιειται το HTTPS, το οποιο κρυπτογραφει τα δεδομενα που αποστελλονται στο δικτυο, εξασφαλιζοντας οτι μονο ο server και ο client μπορουν να τα διαβασουν.

Ο development server του Django `manage.py runserver` υποστηριζει μονο http, και γενικα δεν προοριζεται για χρηση ως production server.

Ως production server θα χρησιμοποιησουμε τον `apache`, ο οποιος υποστηριζει SSL, καθως και το standard WSGI, το οποιο χρησιμοποιειται απο το Django για την διαχειριση εισερχομενων requests.

## Εγκατασταση απαραιτητων πακετων

Αν δεν εχουν ηδη εγκατασταθει:

```
sudo apt-get install apache2 apache2-dev libapache2-mod-wsgi
pip install mod-wsgi
```


## Self-signed certificate

Για να μπορει να δεχτει και να εξυπηρετησει HTTPS συνδεσεις, ο server χρειαζεται ενα SSL certificate. Για λογους απλοτητας χρησιμοποιουμε self-signed certificate. Η διαδικασια παραγωγης ενος self-signed certificate ειναι η παρακατω (δεν χρειαζεται να γινει παλι, τα certificates υπαρχουν στο φακελο `ssl`)

```
# generate private key
$ openssl genrsa -des3 -out server.key 1024

# generate certificate signing request
$ openssl req -new -key server.key -out server.csr

# remove passphrase from key
$ cp server.key server.key.org
$ openssl rsa -in server.key.org -out server.key

# generate self-signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

Τα σημαντικα αρχεια που παραγονται με τον τροπο αυτο ειναι:
* `server.key`, το private κλειδι μας
* `server.crt`, το self-signed certificate μας

## Εκκινηση του server σε https

Η ρυθμιση του apache2 γενικα γινεται πειραζοντας το αρχειο [httpd.conf](https://wiki.apache.org/httpd/DistrosDefaultLayout). Για λογους απλοτητας και φορητοτητας, χρησιμοποιουμε το εργαλειο `mod_wsgi-express`.

Μεσα απο το virtual environment:

```
# create directory for static files (.css, .js, etc)
python manage.py collectstatic

# run server at https://asoures.gr:8443
mod_wsgi-express start-server \
    --log-to-terminal --startup-log \
    --https-port 8443 --https-only --server-name asoures.gr \
    --ssl-certificate-file ssl/server.crt \
    --ssl-certificate-key-file ssl/server.key \
    --url-alias /static static \
    --application-type module project.wsgi
```

Για να μην χρειαζεται να γραφουμε συνεχεια την εντολη αυτη, εχει ενσωματωθει σαν custom management command στο django:

```
python manage.py runhttps 8443
```

Ο server πλεον ακουει στη διευθυνση `https://asoures.gr:8443`.

## Ρυθμιση των hosts

Το certificate δημιουργειται για ενα συγκεκριμενο ονομα διευθυνσης. Τo certificate που υπαρχει στο φακελο `ssl/` δημιουργηθηκε για domain name `asoures.gr`. Οι αιτησεις στο server πρεπει να γινονται μεσω αυτου του ονοματος. Για να πηγαινουν τα αιτηματα στο server, πρεπει:

```
# ρυθμιση του hostfile, δεν χρειαζεται καθε φορα
sudo echo "127.0.0.1 asoures.gr" >> /etc/hosts
```

Τωρα, ολες οι αιτησεις προς το domain `asoures.gr` θα ανακατευθυνονται στο `localhost`, εκει δηλαδη οπου τρεχει ο server μας.

## Χρηση του server πανω απο https

### Για curl

Το curl γκρινιαζει επειδη δεν μπορει να πιστοποιηθει το self-signed certificate. Για να το ξεπερασουμε:

*   Α Τροπος (Ζηταμε το certificate και το χρησιμοποιουμε σε ολα τα requests)

    ```
    $ echo quit | openssl s_client -showcerts -servername asoures.gr -connect asoures.gr:8443 > cacert.pem

    # do request
    $ curl --cacert cacert.pem https://asoures.gr:8443/observatory/api/login/ -d 'username=USER&password=PASS'
    ```

*   Β Τροπος (Επιτρεπουμε τη χρηση μη πιστοποιημενου certificate)

    ```
    $ curl --insecure https://asoures.gr:8443/observatory/api/login/ -d 'username=USER&password=PASS'
    ```

### Για browser

Αν ανοιξεις οποιονδηποτε browser σε καποια σελιδα του server (π.χ. στο [admin](https://asoures.gr:8443/admin)), θα βγαλει μηνυμα οτι η συνδεση δεν ειναι ασφαλης (ERR_CERT_AUTHORITY_INVALID, επειδη το certificate δεν ειναι πιστοποιημενο). Απλα αποδεξου τη συνδεση (π.χ. στον Chrome `Advanced` > `Proceed to asoures.gr`)

## Πηγες / Αναφορες

* http://blog.dscpl.com.au/2015/04/introducing-modwsgi-express.html
* https://wiki.apache.org/httpd/DistrosDefaultLayout
* https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/modwsgi/
* https://stackoverflow.com/questions/27611193/use-self-signed-certificate-with-curl
* https://gist.github.com/GrahamDumpleton/b79d336569054882679e
