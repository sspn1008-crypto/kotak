import winston from 'winston';
import config from './config.js';

const logger = winston.createLogger({
  level: config.logging.level,
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.splat(),
    winston.format.json(),
    winston.format.colorize()
  ),
  defaultMeta: { service: 'tradingview-kotak' },
  transports: [
    new winston.transports.File({ 
      filename: 'logs/error.log', 
      level: 'error',
      format: winston.format.uncolorize()
    }),
    new winston.transports.File({ 
      filename: 'logs/combined.log',
      format: winston.format.uncolorize()
    }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

export default logger;
