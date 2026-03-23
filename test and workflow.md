# Explication du Workflow & Automation des test

- **on: [push, pull_request]**  
  Déclenche les tests à chaque push ou pull request.

- **runs-on: ubuntu-latest**  
  Utilise une machine Ubuntu pour exécuter les tests.

- **actions/checkout@v3**  
  Clone le code du dépôt pour que le workflow puisse y accéder.

- **actions/setup-python@v3**  
  Installe Python, nécessaire pour exécuter les tests et les scripts.

- **pip install -r requirements.txt**  
  Installe les dépendances Python spécifiées dans le fichier `requirements.txt`.

- **pytest test/**  
  Exécute les tests unitaires en utilisant Pytest sur le répertoire `test/`.
