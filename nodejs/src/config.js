import dotenv from 'dotenv';

dotenv.config();

const config = {
  kotak: {
    apiKey: process.env.KOTAK_API_KEY,
    apiSecret: process.env.KOTAK_API_SECRET,
    clientId: process.env.KOTAK_CLIENT_ID,
    password: process.env.KOTAK_PASSWORD,
    consumerKey: process.env.KOTAK_CONSUMER_KEY,
    consumerSecret: process.env.KOTAK_CONSUMER_SECRET,
    baseUrl: process.env.KOTAK_BASE_URL || 'https://api.kotaksecurities.com/v1'
  },

  webhook: {
    secret: process.env.WEBHOOK_SECRET || 'your-webhook-secret'
  },

  server: {
    port: parseInt(process.env.PORT || '5000', 10),
    nodeEnv: process.env.NODE_ENV || 'development'
  },

  order: {
    defaultQuantity: parseInt(process.env.DEFAULT_ORDER_QUANTITY || '1', 10),
    stopLossPercentage: parseFloat(process.env.STOP_LOSS_PERCENTAGE || '2.0'),
    targetPercentage: parseFloat(process.env.TARGET_PERCENTAGE || '5.0'),
    orderType: process.env.ORDER_TYPE || 'MARKET'
  },

  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};

export default config;
