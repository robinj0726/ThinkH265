global g_nSymbolCounter
g_nSymbolCounter = 0

def GET_SYMBOL_COUNT():
    return g_nSymbolCounter

def INC_SYMBOL_COUNT():
    global g_nSymbolCounter
    g_nSymbolCounter += 1