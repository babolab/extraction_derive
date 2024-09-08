# Extraction de dérive Mothy heure par heure
## Script
Le script `extraction_mothy.py` permet d'extraire les dérives Mothy, qui comportent plusieurs points et plusieurs heures, en un fichier par heure de dérive, afin d'afficher de façon claire les situations à une heure donnée.
Tous les afficheurs ne disposent pas d'une gestion temporelle de l'affichage (ANAIS, Monitorfish par exemple).
### Mode d'emploi
- Télécharger le fichier GPX depuis le site Mothy
- déposer le fichier `rposi.gpx` dans le présent dossier
- Lancer le script python `extraction_mothy.py`
- Les fichiers extraits sont présents dans le dossier courant.
- Si vous souhaitez faire d'autres dérives, lancez un nouvel environnement ou supprimez les fichiers de dérive précédents.
## Application streamlit
L'extraction peut aussi se faire via une application Streamlit, disponible [ici](https://mothyhoraire.streamlit.app/).