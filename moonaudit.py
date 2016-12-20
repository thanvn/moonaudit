# moonaudit
#
# install deps using pip:
# python-bitcoinrpc, json

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import time

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# user-config section
rpchost = '127.0.0.1'
rpcuser = 'rpcuser'
rpcpass = 'rpcpass'
txnconf = 5

print ""
curblock=0
rpcpipe = AuthServiceProxy('http://' + rpcuser + ':' + rpcpass + '@' + rpchost + ':44663')
while(1!=2):
   curblock=curblock+1
   totalblk=rpcpipe.getblockcount()
   if (curblock>totalblk-txnconf):
      while(1!=2):
         time.sleep(5)
         totalblk=rpcpipe.getblockcount()
         if (curblock==totalblk-txnconf):
            break
   rawblockhash=rpcpipe.getblockhash(curblock)
   rawblockdata=rpcpipe.getblock(rawblockhash)
   timestamp=find_between(str(rawblockdata),'time\': ',', u\'bits')
   sendnum=0
   for txhash in rawblockdata['tx']:
       sendnum=sendnum+1
       txraw=rpcpipe.getrawtransaction(txhash)
       txdata=rpcpipe.decoderawtransaction(txraw)
       curvout=-1
       for outputs in txdata['vout']:
            curvout=curvout+1
            address = ''
            value = 0 
            address = find_between(str(outputs), '[u\'', '\']')
            value = find_between(str(outputs), 'Decimal(\'', '\')')
            if (float(str(value))>28999999.99999999):
               print 'block number: %08d;' % (curblock,) + ' unixtime: ' + timestamp + '; address: ' + address + '; coins sent in one operation: ' + str(value) + '; txid of transaction: ' + txhash
