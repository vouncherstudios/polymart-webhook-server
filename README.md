# Polymart Webhook Server

A lightweight server to receive and validate Polymart webhooks, and forward the formatted information to a Discord channel.

## Features

- Receives webhooks from Polymart
- Validates webhook signatures
- Forwards formatted information to a Discord channel

## Requirements

These requirements is only applicable if you are running from outside Glitch.

- Python 3.x

## Local Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/polymart-webhook-server.git
   cd polymart-webhook-server
   ```

2. Install the dependencies:

   ```sh
   pip install -r .requirements.txt
   ```

3. Copy the `.env.example` file to `.env` and fill in your configuration:

   ```sh
   cp .env.example .env
   ```

4. Update the `.env` file with your Polymart webhook secrets and Discord webhook URL:
   ```env
   WEBHOOK_SECRET_SPLITTER=YOUR_SPLITTER
   WEBHOOK_SECRETS=YOUR_SECRETS
   DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
   DISCORD_PURCHASE_WEBHOOK_CONTENT=YOUR_DISCORD_WEBHOOK_CONTENT
   DISCORD_REFUND_WEBHOOK_CONTENT=YOUR_DISCORD_WEBHOOK_CONTENT
   ```

## Glitch Setup

To set up the server on Glitch, follow these steps:

1. Create a new Glitch project by going to [glitch.com](https://glitch.com) and clicking on "New Project".

2. Choose "Import from GitHub" and paste the URL (`https://github.com/yourusername/polymart-webhook-server.git`).

3. Wait for the project to import and click on "Show" to open the project editor.

4. Open the `.env` file and add the following configuration:

   ```env
   WEBHOOK_SECRET_SPLITTER=YOUR_SPLITTER
   WEBHOOK_SECRETS=YOUR_SECRETS
   DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
   DISCORD_PURCHASE_WEBHOOK_CONTENT=YOUR_DISCORD_WEBHOOK_CONTENT
   DISCORD_REFUND_WEBHOOK_CONTENT=YOUR_DISCORD_WEBHOOK_CONTENT
   ```

5. Finally, click on "Tools" again and select "Logs" to see the server logs. Your server should now be running on Glitch.

Do not share your `.env` file or webhook secrets publicly.

## Running the Server

Start the server using the following command:

```sh
python server.py
```

The server will run on `http://0.0.0.0:5000` by default.

## Usage

The server exposes a single endpoint `/` to receive POST requests from Polymart webhooks. It validates the webhook signature and forwards the formatted information to the specified Discord channel.

## Environment Variables

- `WEBHOOK_SECRET_SPLITTER`: The webhook secret splitter. 
- `WEBHOOK_SECRETS`: Your Polymart webhook secrets.
- `DISCORD_WEBHOOK_URL`: The URL of your Discord webhook.
- `DISCORD_PURCHASE_WEBHOOK_CONTENT`: The JSON payload template for purchase events.
- `DISCORD_REFUND_WEBHOOK_CONTENT`: The JSON payload template for refund events.

## License

Polymart Webhook Server is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
