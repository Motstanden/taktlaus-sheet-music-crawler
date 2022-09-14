# Summary
The purpose of this project was to crawl the previous version of [taktlaus.no](https://taktlaus.no/) for sheet music files.
The code is now broken because the target website has been rewritten, and this code is not maintained (at all). 

**Beware of extremely ugly code if you decide to venture further into this repo.**

# Setup
1. Set opp et *virtual environment*
    ```
    python -m venv .venv
    source .venv/scripts/activate
    ```
2. Installer de nødvendige bibliotekene
    ```
    pip install --requirement requirements.txt
    ```
3. Lag en fil som heter .env, og legg til brukernavn og passord. Filen skal ha dette innholdet
    ```
    TAKTLAUS_USERNAME=DITT_BRUKERNAVN_TIL_TAKTLAUS_SIDEN
    TAKTLAUS_PASSWORD=DITT_PASSORD_TIL_TAKTLAUS_SIDEN
    ```
4. Kjør script
    ```
    python main.py
    ```

# E-post-varsel
Crawler-en kan sende e-post-varsel når den har oppdaget nye- eller oppdaterte noter. Følg disse stegene for å sette opp e-post-varsel.  

1. Lag en dummy-e-post-konto som crawler-en kan bruke til å sende e-post gjennom. I skrivende stund er det bare testet med gmail-kontoer

2. Legg til brukernan og passord for e-post-kontoen `.env` filen. Teksten du legger til skal se ut som dette:
    ```
    EMAIL_USERNAME=BRUKERNAVN_TIL_E_POST_KONTOEN_DIN
    EMAIL_PASSWORD=PASSORD_TIL_E_POST_KONTOEN_DIN
    ```
3. Sørg for at e-post-kontoen du bruker tillater `SMTP`. For gmail-kontoer kan [denne guiden](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/) følges. 
