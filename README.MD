# Slack Integration Process

1. **Redirect to:**  
   [Slack API Apps](https://api.slack.com/apps)

2. **Create a New App:**  
   Click on the "Create New App" button.  
   Select "From scratch" and click on it.

3. **Enter App Details:**  
   - Enter the App Name.  
   - Select the workspace.  
   - Click on the "Create App" button.

4. **App Creation:**  
   The app will be created, and you will be redirected to:  
   `https://api.slack.com/apps/#app_id`

5. **Configure OAuth & Permissions:**  
   - Select **OAuth & Permissions** from the left sidebar.  
   - Scroll down to find the **Scopes** section under **Bot Token Scopes**.  
   - Add the `chat:write` scope.

6. **Set Up Event Subscription:**  
   - Select **Event Subscriptions** and enable it.  
   - Add the HTTPS base URL for the requested redirection:  
     `https://<your-ngrok-url>/slack/events`  
     *(If you are using a development server, use Ngrok for the secured HTTP URL.)*  
   - In the **Subscribe to bot events** section, add the `message.channels` event.  
   - Click on **Save Changes**.

7. **Reinstall the App:**  
   After clicking **Save Changes**, you will receive information to reinstall the app.  
   Reinstall the app to apply the changes.

8. **Obtain Keys and Tokens:**  
   - In **Basic Information**, you will find the **Client ID**, **Client Secret**, and **Signing Secret**.  
   - In **OAuth & Permissions**, you will get the **User OAuth Token** and **Bot User OAuth Token**.

9. **Add the App to a Channel:**  
   Create a public channel and use the message format:  
   `/invite @<AppName>` to add the app to the channel.

10. **Run the Flask App:**  
    Start your Flask app to begin interacting with Slack.
