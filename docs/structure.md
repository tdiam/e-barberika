# Δομή project

* `docs/`  
  Documentation που αφορά όλο το project πρέπει να αποθηκεύεται εδώ και να είναι γραμμένο σε Markdown. Για επιμέρους modules, μπορεί το documentation να υπάρχει μόνο στον κώδικά τους.
* `project/`
    * `settings/`  
      Module για τις ρυθμίσεις που διαβάζει από το *.env* και εξάγει τις παραμέτρους ρύθμισης στο Django.
    * `urls.py`  
      Οδηγίες για το top-level routing.
* `manage.py`  
  Εργαλείο command-line για το Django.
* `pylintrc`  
  Αρχείο ρύθμισης για το Pylint.
* `env.sample`  
  Παράδειγμα αρχείου ρύθμισης *.env*.
* `_version.py`  
  Περιέχει μια μεταβλητή `__version__` όπου αποθηκεύεται η τρέχουσα έκδοση του project. Χρησιμοποιείται calendar versioning.
* `setup.py`  
  Script εγκατάστασης.
* `requirements.txt`  
  Pinned production dependencies.
* `requirements-dev.txt`
  Pinned development dependencies.