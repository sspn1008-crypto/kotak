const SYMBOL_MAPPING = {
  'SBIN': 'SBIN-EQ',
  'RELIANCE': 'RELIANCE-EQ',
  'INFY': 'INFY-EQ',
  'TCS': 'TCS-EQ',
  'WIPRO': 'WIPRO-EQ',
  'HDFC': 'HDFC-EQ',
  'ICICIBANK': 'ICICIBANK-EQ',
  'LT': 'LT-EQ',
  'MARUTI': 'MARUTI-EQ',
  'BAJAJ-AUTO': 'BAJAJ-AUTO-EQ',
  'NIFTY': 'NIFTY50-IX',
  'BANKNIFTY': 'BANKNIFTY-IX',
  'FINNIFTY': 'FINNIFTY-IX',
  'MIDCPNIFTY': 'MIDCPNIFTY-IX'
};

export function getKotakSymbol(tvSymbol) {
  const symbol = tvSymbol.toUpperCase();
  return SYMBOL_MAPPING[symbol] || `${symbol}-EQ`;
}

export function addSymbolMapping(tvSymbol, kotakSymbol) {
  SYMBOL_MAPPING[tvSymbol.toUpperCase()] = kotakSymbol;
}

export function getSymbolMappings() {
  return { ...SYMBOL_MAPPING };
}
