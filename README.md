# Summary
The purpose of this project was to crawl the previous version of [taktlaus.no](https://taktlaus.no/) for sheet music files.
The code is now broken because the target website has been rewritten, and this code is not maintained (at all). 

**Beware of ugly code if you decide to venture further into this repo.**

# Setup
1. Set up a *virtual environment*
    ```
    python -m venv .venv
    source .venv/scripts/activate
    ```
2. Install required dependencies
    ```
    pip install --requirement requirements.txt
    ```
3. Create a `.env` file, and add your username and password for taktlaus.no. The file should have the following content:
    ```
    TAKTLAUS_USERNAME=<your-username-goes-here>
    TAKTLAUS_PASSWORD=<your-passowrd-goes-here>
    ```
4. Run script
    ```
    python main.py
    ```

# Email notification
The craweler can send email notification if it detects that Dei Taktlause has uploaded or updated any files. Do the following steps to set this up: 

1. Create a dummy gmail account that the crawler can use.

2. Append your email and passowrd information to the `.env` file. The appended text should look like this:
    ```
    EMAIL_USERNAME=<your-email-address-goes-here>
    EMAIL_PASSWORD=<your-email-password-goes-here>
    ```
3. Ensure that **SMTP** is allowed on your gmail account. Use [this guide](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/) to set up *SMTP*. 
