UPDATE telephony_configurations SET credentials = jsonb_set(credentials::jsonb, '{api_base}', '"https://app.voicelink.co.in/api"') WHERE provider = 'voicelink';
