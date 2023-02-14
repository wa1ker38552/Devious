# Devious
*Devious Selfbot v7 😈*

**Warning ⚠️** <br>
*Selfbots are against Discord's TOS, use at your own risk! Recommended that you run on an alt.*

**Setup ⚙️** <br>
`git clone https://github.com/wa1ker38552/devious` <br>
`pip install discord-py==1.7.3` (Use cached version on Replit) <br>
`pip install discord==1.7.3`

**Replit** <br>
1. Clone this repository
2. Create a new environmental variable called `TOKEN` and set it to your Discord token
3. In shell, run `pip install discord==1.7.3`, `pip install discord-py==1.7.3`
<br><br>> *It's recommended that you run a ping script to keep the bot alive for extended periods of time*

**Features ✨**
- Error handling and messages
- Message intents bypass
- Auto-generated help command
- Custom database class
- Configuration file
- Easily customizable with cogs

**Notes 📝** <br>
- Fast response times are achived by only scanning messages from the client.
- **Only** the client is able to send commands.
- To bypass message intents which are blocked for regular users on Discord-py, you can scan message channel history to find the most recently posted message.
- Discord-py 1.7.3 was the last version that supported selfbots.
- Environmental PATH for token is set in `config.json` not the actual token.
