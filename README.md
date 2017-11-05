# Give a gift

Randomly select who will give a gift to whom.

* Support couples and single persons.
* Send a email to the persons who will give a gift.
* Backup the results into a file. Use it next time to avoid same results.

## Prerequisites

* Python version >= 3.5

* To send emails, you need a `Sendgrid` account or a `SendinBlue` account or a 
  `Gmail` account
  
  * If you have a `Sendgrid` account, update the development environment 
    with your `SENDGRID_API_KEY`:
    
    ```bash
    $ export SENDGRID_API_KEY=xxxx
    ```
    
  * If you have a `SendinBlue` account, update the development environment 
    with your `SENDINBLUE_API_KEY_V3`:
    
    ```bash
    $ export SENDINBLUE_API_KEY_V3=xxxx
    ```
    
  * If you have a `Gmail` account, update the development environment with your 
    `GMAIL_USER` and `GMAIL_PASSWORD`:
    
    ```bash
    $ export GMAIL_USER=xxxx
    $ export GMAIL_PASSWORD=yyyy
    ```

## Usage

First:

    $ cp sample_settings.py settings_my_family.py

Edit `settings_my_family.py`, then:

    $ python3 give_a_gift.py settings_my_family.py
    $ python3 give_a_gift.py settings_dulac.py --apply


## License

[The MIT License (MIT)](LICENSE.txt)
