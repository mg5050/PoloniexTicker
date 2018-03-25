PAIRS = {'BTC_MAID': 51, 'BTC_BURST': 15, 'BTC_PPC': 75, 'ETH_ZEC': 179, 'BTC_NXC': 183, 'USDT_BTC': 121,
         'BTC_ZEC': 178, 'ETH_CVC': 195, 'BTC_DOGE': 27, 'BTC_PASC': 184, 'BTC_XVC': 98, 'BTC_EMC2': 28, 'BTC_GAME': 38,
         'XMR_LTC': 137, 'BTC_CLAM': 20, 'BTC_GNO': 187, 'BTC_BELA': 8, 'USDT_XMR': 126, 'BTC_XMR': 114,
         'BTC_ARDR': 177, 'ETH_REP': 176, 'BTC_LSK': 163, 'BTC_STORJ': 200, 'USDT_ETC': 173, 'USDT_ZEC': 180,
         'BTC_DCR': 162, 'BTC_RIC': 83, 'USDT_XRP': 127, 'BTC_FCT': 155, 'USDT_NXT': 124, 'BTC_NMC': 64, 'BTC_SBD': 170,
         'ETH_GNT': 186, 'USDT_ETH': 149, 'BTC_OMNI': 58, 'BTC_OMG': 196, 'BTC_LBC': 167, 'BTC_SC': 150, 'BTC_GRC': 40,
         'BTC_ETC': 171, 'BTC_BTS': 14, 'BTC_VIA': 97, 'BTC_ZRX': 192, 'BTC_STR': 89, 'XMR_MAID': 138, 'XMR_BLK': 130,
         'XMR_BCN': 129, 'BTC_GNT': 185, 'BTC_PINK': 73, 'BTC_STRAT': 182, 'BTC_NAV': 61, 'BTC_XRP': 117,
         'USDT_BCH': 191, 'BTC_BCY': 151, 'BTC_RADS': 158, 'BTC_DGB': 25, 'BTC_BTM': 13, 'USDT_DASH': 122,
         'ETH_BCH': 190, 'XMR_BTCD': 131, 'BTC_XEM': 112, 'BTC_NXT': 69, 'USDT_REP': 175, 'BTC_GAS': 198, 'BTC_VRC': 99,
         'ETH_GNO': 188, 'BTC_LTC': 50, 'BTC_NEOS': 63, 'ETH_ETC': 172, 'BTC_EXP': 153, 'BTC_XBC': 104,
         'BTC_STEEM': 168, 'ETH_ZRX': 193, 'ETH_STEEM': 169, 'BTC_REP': 174, 'BTC_BCN': 7, 'BTC_FLDC': 31,
         'BTC_ETH': 148, 'BTC_AMP': 160, 'XMR_NXT': 140, 'BTC_BTCD': 12, 'ETH_GAS': 199, 'BTC_SYS': 92, 'XMR_DASH': 132,
         'ETH_OMG': 197, 'BTC_POT': 74, 'BTC_CVC': 194, 'USDT_STR': 125, 'BTC_FLO': 32, 'BTC_XCP': 108, 'BTC_BLK': 10,
         'BTC_BCH': 189, 'XMR_ZEC': 181, 'ETH_LSK': 166, 'USDT_LTC': 123, 'BTC_XPM': 116, 'BTC_DASH': 24,
         'BTC_VTC': 100, 'BTC_HUC': 43} # scraped from Poloniex homepage

def lookupCCYCode(pair):
    try:
        return PAIRS[pair]
    except KeyError:
        raise Exception('Currency pair does not exist.')