# Client

Το project περιέχει δύο "εφαρμογές", τον client και τον server. Τρέχουν ανεξάρτητα η μία από την άλλη, άρα έχουν διαφορετικές IP/θύρες. Ο Client μας είναι χτισμένος σε NodeJS + React και δημιουργήθηκε με το [`create-react-app`](https://reactjs.org/docs/create-a-new-react-app.html). Βρίσκεται στον φάκελο `project/client/`.

Ο client δεν συνδέεται με το υπόλοιπο Django project του server, απλά χρησιμοποιεί το API του, όπως θα μπορούσε να χρησιμοποιεί ένα οποιοδήποτε άλλο API.

## Εντολές

Για να ξεκινήσουμε τον client, μπαίνουμε στον φάκελο `project/client/` και τρέχουμε:
```
npm run start
```

## TODO

Δεν έχει ολοκληρωθεί ούτε καν το σετάρισμα -- λείπουν βασικά κομμάτια:
- Module για επικοινωνία με το API
- Σετάρισμα routing
- Stage management (?)