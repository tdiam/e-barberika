## Χρήση

Για να ξεκινήσεις τον server, εκτέλεσε την εντολή:
```
$ manage.py runserver 8000
```

O server ακουει στη διευθυνση `http://localhost:8000/`

## Xρήση με SSL

[Περισσοτερα εδω](ssl.md)

Για να τρέξεις τον server πάνω από https:

```
# ρυθμιση του hostfile, δεν χρειαζεται καθε φορα
sudo echo "127.0.0.1 asoures.gr" >> /etc/hosts
```

Έπειτα, για να τρεξει ο server:

```
manage.py runhttps 8443
```

Ο server ακουει στη διευθυνση `https://asoures.gr:8443/`.