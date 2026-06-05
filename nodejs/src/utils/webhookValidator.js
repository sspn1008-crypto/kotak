import crypto from 'crypto';
import logger from '../logger.js';

export function validateWebhookSignature(data, signature, secret) {
  try {
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(data)
      .digest('hex');

    const isValid = crypto.timingSafeEqual(
      Buffer.from(expectedSignature),
      Buffer.from(signature)
    );

    if (!isValid) {
      logger.warn('Invalid webhook signature detected');
    }

    return isValid;
  } catch (error) {
    logger.error('Webhook signature validation error:', error);
    return false;
  }
}

export function generateSignature(payload, secret) {
  const data = JSON.stringify(payload);
  return crypto
    .createHmac('sha256', secret)
    .update(data)
    .digest('hex');
}
