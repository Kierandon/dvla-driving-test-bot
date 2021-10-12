This was hacked together in not a good way.

Selenium is required.
discord.py is required.

```
"Licence": "", # Full UK Driving Licence
"Booking_Ref": "", # Current Test Booking Reference
"Test_Center": "", # Test Center Name / Postcode
```

is defined in two functions, `async def on_message(message):` and `async def testCheck():` and you have to manually input those values in the
code, lol.

Your discord bot token also has to be defined (line 181)

The channel to send 30 minute updates into also has to be defined (line 99)
