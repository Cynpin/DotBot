# DotBot Info

**DotBot** is a bot that can generate a dot voting message to help schedule events easily. Dot voting messages have a title, body text and a list of dates. Every date has an emoji behind it, all the emoji's used will also be added to the message as reactions after posting by DotBot. People in the server can now signal their availability for the mentioned evenings by pressing the reactions.

It will look something like this:

![image](https://github.com/user-attachments/assets/c7d19a35-742e-47bc-a17b-fc2d553a0a32)

PS. if you want to use this code, you need to make an .env file and put your own bot token in there.

## Command: `!dot`

Typing `!dot` will generate a message with:
- A list of dates for the next **10 days**
- A **unique emoji** behind each date

---

## Custom Inputs

You can customize your dot voting message with the following options:

### Amount of Days  
Add a number between **1–18** after `!dot` to change how many days are shown.  
Example: `!dot 5` will show 5 days instead of the default 10.

### Start Date  
Specify a custom start date in the format:  
`DD-MM` or `DD-MM-YYYY`  
The month can be a **number**, an **abbreviation**, or **written fully**.

> Including the year is recommended if you're voting in December.

### Title and Content  
You can include a **title** and **content** by using **quoted text**:
- The **first quoted text** is used as the **title**
- The **second quoted text** is used as the **message content**

Example:
```  
!dot "Team Meeting" "Please vote for your available dates.
Use Shift+Enter to add new lines."
```
Just make sure to **close your quotation marks** properly!

### @no-one  
Add `@no-one` to make a **test message**.  
This prevents DotBot from tagging everyone (by default, it will tag everyone).

---

## Order of Inputs

Inputs can go in **any order** and can be included or omitted as needed.  
**Note:** If you're changing the content, the **title must always come before the content**.
